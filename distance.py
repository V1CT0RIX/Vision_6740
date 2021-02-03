import math as m

#a1 = camera angle, a2 = Y angle to the target, th = target height, ch = camera height,
def dist(angle,th,ch):
    if angle == 0:
        return 0
    else:
        distance = ((th-ch)/m.tan(angle))
        print(distance)

    return distance

#px, py specify the point to convert to angles. camera is a list dictionary which contains {"resx":, "resy":, "hfov":, "vfov":}
def PixelsToAngles(px,py, camera):
    '''
    print("px:"+str(px)+"\n")
    print("py:"+str(py)+"\n")
    '''

    hfov = m.radians(camera["hfov"])
    vfov = m.radians(camera["vfov"])

    #convert between regular to normalized pixels
    nx = ((px-(camera["resx"]/2))/(camera["resx"]/2))
    ny = (((camera["resy"]/2-py))/(camera["resy"]/2))
    #print("nx: "+str(nx)+"\nny: "+str(ny)+"\n\n")

    Xangle = m.atan(m.tan(hfov/2)*nx)
    Yangle = m.atan(m.tan(vfov/2)*ny)
    #print("Xangle: "+str(m.degrees(Xangle))+"\nYangle: "+str(m.degrees(Yangle))+"\n\n")

    return Xangle, Yangle

def force(th,ch,d):
    g = 9.823

    t = m.sqrt((2*(th-ch))/g)

    v = m.sqrt((g*t)**2+(d/t)**2)

    a = m.radians(90) - m.atan((g*(t**2))/d)

    '''
    # H = Hw-Hr
    v = m.sqrt(g*(4*(H**2)+(d**2))/(2*H))

    a = m.atan((2*H)/d)
    '''

    return (m.degrees(a),k*v)

'''
#test
camera = {"resx": 1920, "resy": 1080, "hfov": 60, "vfov": 68.5}
x,y = PixelsToAngles(480,0,camera)
d = dist(y, 2, 0.5)
print((x/math.pi)*360)
'''
