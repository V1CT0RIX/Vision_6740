import image_processor as ip
import cv2
import distance
import numpy

cameraprop = {"resx": 640, "resy": 480, "hfov": 67.7, "vfov": 53.4}
camera = cv2.VideoCapture(0)
while True:

    _, input_img = camera.read()

    thresholded_img = ip.clear_noize((ip.threshold(input_img, (19,64,149), (54,164,255))), 200)
    cv2.imshow("threshold", thresholded_img)


    detected_shapes_img, detected_shapes = ip.detect_shapes(input_img, thresholded_img, 4, 200, 0.05)

    if len(detected_shapes) > 0:
        M = cv2.moments(thresholded_img)
        center = [int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"])]
        _, angle = distance.PixelsToAngles(center[0],center[1], cameraprop)
        cv2.imshow("detected", cv2.circle(detected_shapes_img, tuple(center), 2, (255,0,0)))

        print(distance.dist(angle, 10.25, 5))


    cv2.waitKey(1)

cv2.destroyAllWindows()
