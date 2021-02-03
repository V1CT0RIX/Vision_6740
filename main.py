import cv2
import numpy as np
import distance
from skimage import morphology
from networktables import NetworkTables
from cscore import CameraServer
import logging

def main():
    logging.basicConfig(level=logging.DEBUG)
    NetworkTables.initialize(server="10.0.0.3")
    sd = NetworkTables.getTable("SmartDashboard")
    do_image_processing = sd.getAutoUpdateValue("do_image_processing", 0)
    stream_type = sd.getAutoUpdateValue("stream_type", 0)
    threshold_parameters = sd.getAutoUpdateValue("threshold_parameters", 0)

    cameraprop = {"resx": 640, "resy": 480, "hfov": 67.7, "vfov": 53.4}

    cs = CameraServer.getInstance()
    cs.enableLogging()

    # Capture from the first USB Camera on the system
    camera = cs.startAutomaticCapture()
    camera.setResolution(320, 240)

    # Get a CvSink. This will capture images from the camera
    cvSink = cs.getVideo()

    # (optional) Setup a CvSource. This will send images back to the Dashboard
    outputStream = cs.putVideo("Name", 320, 240)

    # Allocating new images is very expensive, always try to preallocate
    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

    while True:
        # Tell the CvSink to grab a frame from the camera and put it
        # in the source image.  If there is an error notify the output.
        time, img = cvSink.grabFrame(img)
        if time == 0:
            # Send the output the error.
            outputStream.notifyError(cvSink.getError())
            # skip the rest of the current iteration
            continue

        if do_image_processing.value:
            img = image_processor(img, sd, cameraprop, stream_type, threshold_parameters)

        # (optional) send some image back to the dashboard
        outputStream.putFrame(img)


def image_processor(input_img, sd, cameraprop, stream_type, threshold_parameters):
    #declar inerfunctions
    def threshold(img, p_lower_limit, p_upper_limit):
        lower_limit = np.array(p_lower_limit ,np.uint8)
        upper_limit = np.array(p_upper_limit ,np.uint8)

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
    thresholded_img = clear_noize((threshold(input_img, (threshold_parameters[0],threshold_parameters[1],threshold_parameters[2]), threshold_parameters[3],threshold_parameters[4],threshold_parameters[5])), 200)
    #cv2.imshow("threshold", thresholded_img)

    detected_shapes_img, detected_shapes = detect_shapes(input_img, thresholded_img, 4, 200, 0.05)

    if len(detected_shapes) > 0:
        M = cv2.moments(thresholded_img)
        center = [int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"])]

        #calc distance, angles, force
        x_angle, y_angle = distance.PixelsToAngles(center[0],center[1], cameraprop)
        distance = distance.dist(y_angle,th,ch)
        hood_angle, velocity = distance.force(th,ch,distance) #need to set robot and target height

        sd.putValue('shooter', (velocity, hood_angle))
    else:
        sd.putValue('shooter', None)

        center = (-1, -1)

    if stream_type.value == 0:
        return cv2.circle(detected_shapes_img, tuple(center), 2, (255,0,0))
    else:
        return thresholded_img
