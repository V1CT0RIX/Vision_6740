import math as m

Hr = 0.5
Hw = 2.5
d = 2.21
k = 1

g = 9.823

def Tconstant(Hr,Hw,d,g):
    return m.sqrt((2*(Hw-Hr))/g)

def force(d,t):

    v = m.sqrt((g*t)**2+(d/t)**2)

    a = m.radians(90) - m.atan((g*(t**2))/d)

    '''
    # H = Hw-Hr
    v = m.sqrt(g*(4*(H**2)+(d**2))/(2*H))

    a = m.atan((2*H)/d)
    '''

    return (m.degrees(a),k*v)

def air(row,v,cd,re):
    return(0.5*row*(v**2)*cd*re)

t = Tconstant(Hr,Hw,d,g)
f = force(d,t)
print(f)
