import cv2
import numpy as np
import distance
from skimage import morphology
from networktables import NetworkTables
#from cscore import CameraServer
import logging
import time

def main():
    logging.basicConfig(level=logging.DEBUG)
    NetworkTables.initialize(server="")
    sd = NetworkTables.getTable("SmartDashboard")
    process_image = sd.getAutoUpdateValue("process_image", False)
    stream_type = sd.getAutoUpdateValue("stream_type", False)
    threshold_parameters = sd.getAutoUpdateValue("threshold_parameters", (0,0,0,180,255,255))

    vid = cv2.VideoCapture(0)

    cameraprop = {"resx": 640, "resy": 480, "hfov": 67.7, "vfov": 53.4}


    while True:
        _,img = vid.read()
        print(threshold_parameters.value,process_image.value,stream_type.value)
        if process_image.value:
            img = image_processor(img, sd, cameraprop, stream_type, threshold_parameters.value)

        cv2.imshow('frame',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        t = time.time()
        while time.time()-t < 0.02:
            continue




def image_processor(input_img, sd, cameraprop, stream_type, threshold_parameters):
    #declar inerfunctions
    def threshold(img, threshold):

        lower_limit = np.array(threshold[0:3] ,np.uint8)
        upper_limit = np.array(threshold[3:7] ,np.uint8)

        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        frame_threshed = cv2.inRange(hsv_img, lower_limit, upper_limit)

        return frame_threshed

    def clear_noize(img, max_noize_size):
        img = morphology.label(img) # create labels in segmented image
        cleaned = morphology.remove_small_objects(img, min_size=max_noize_size, connectivity=2)

        img = np.zeros((cleaned.shape)) # create array of size cleaned
        img[cleaned > 0] = 255
        img = np.uint8(img)

        return img

    def detect_shapes(img, thresholded_img, sides_num, min_area, approx_epsilon):
        detected_shapes_img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)

        contours,_ = cv2.findContours(thresholded_img, cv2.RETR_TREE,
                                    cv2.CHAIN_APPROX_SIMPLE)
        # Searching through every region selected to
        # find the required polygon.
        detected_shapes = []
        for cnt in contours :
            approx = cv2.approxPolyDP(cnt,
                                    approx_epsilon * cv2.arcLength(cnt, True), True)

            # Checking if the no. of sides of the selected region is 7.
            if(len(approx) == sides_num) and (detected_shapes_img.shape[0]-1)*(detected_shapes_img.shape[1]-1) > cv2.contourArea(cnt) and min_area < cv2.contourArea(cnt):
                cv2.drawContours(detected_shapes_img, [approx], 0, (0, 0, 255), 1)
                detected_shapes.append(approx)

        return detected_shapes_img, detected_shapes

    #function code
    thresholded_img = clear_noize(threshold(input_img, threshold_parameters), 400)


    detected_shapes_img, detected_shapes = detect_shapes(input_img, thresholded_img, 4, 200, 0.05)

    if len(detected_shapes) > 0:
        M = cv2.moments(thresholded_img)
        center = [int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"])]

        #calc distance, angles, force
        th,ch,k = 2,1,1
        x_angle, y_angle = distance.PixelsToAngles(center[0],center[1], cameraprop)
        dist = distance.dist(y_angle,th,ch)
        hood_angle, velocity = distance.force(th,ch,dist) #need to set robot and target height

        sd.putValue('shooter', (velocity, hood_angle, x_angle, y_angle))
    else:
        sd.putValue('shooter', (-1,-1,-1,-1))

        center = (-1, -1)

    if stream_type.value == False:
        return cv2.circle(detected_shapes_img, tuple(center), 2, (255,0,0))
    else:
        return thresholded_img

main()
