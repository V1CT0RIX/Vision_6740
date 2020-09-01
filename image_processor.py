import cv2
import numpy as np
from skimage import morphology
import distance

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
'''
camera = cv2.VideoCapture(0)
while True:
    _, input_img = camera.read()

    cv2.imshow("input", input_img)

    thresholded_img = clear_noize((threshold(input_img, (0,92,142), (180,255,255))), 150)
    cv2.imshow("threshold", thresholded_img)

    detected_shapes_img, detected_shapes = detect_shapes(input_img, thresholded_img, 4, 200, 0.05)
    cv2.imshow("detectet outlines", detected_shapes_img)

    if len(detected_shapes) > 0:
        shape_center = (sum(point[0] for point in detected_shapes[0])/len(detected_shapes[0]),
                        sum(point[1] for point in detected_shapes[0])/len(detected_shapes[0]))
        print(p2m.PixelsToAngles(shape_center[0], pshape_center[1], input_img.shape))

    cv2.waitKey(1)

cv2.destroyAllWindows()
'''
