import math

#a1 = camera angle, a2 = Y angle to the target, th = target height, ch = camera height,
def dist(angle,th,ch):
    if angle == 0:
        return 0
    else:
        distance = ((th-ch)/math.tan(angle))
        print(distance)

    return distance

#px, py specify the point to convert to angles. camera is a list dictionary which contains {"resx":, "resy":, "hfov":, "vfov":}
def PixelsToAngles(px,py, camera):
    '''
    print("px:"+str(px)+"\n")
    print("py:"+str(py)+"\n")
    '''

    hfov = math.radians(camera["hfov"])
    vfov = math.radians(camera["vfov"])

    #convert between regular to normalized pixels
    nx = ((px-(camera["resx"]/2))/(camera["resx"]/2))
    ny = (((camera["resy"]/2-py))/(camera["resy"]/2))
    #print("nx: "+str(nx)+"\nny: "+str(ny)+"\n\n")

    Xangle = math.atan(math.tan(hfov/2)*nx)
    Yangle = math.atan(math.tan(vfov/2)*ny)
    #print("Xangle: "+str(math.degrees(Xangle))+"\nYangle: "+str(math.degrees(Yangle))+"\n\n")

    return Xangle, Yangle

#test

camera = {"resx": 1920, "resy": 1080, "hfov": 60, "vfov": 68.5}
x,y = PixelsToAngles(480,0,camera)
#d = dist(y, 2, 0.5)
print((x/math.pi)*360)
