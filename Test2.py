import math

import rt
from Point import Point


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return ang + 360 if ang < 0 else ang


def getDyDx(pA, pB):
    dx = pB.x - pA.x
    dy = pB.y - pA.y
    return Point(dx, dy)


#light = Point(14,5)
light = Point(11,9)

a = Point(11,8)
b = Point(5.2844650363276, 5.7185842823965)

originPoint = Point(9, 10)
lightRay = Point(-1, -5) #Light vector also direction






#----------------------------------------------------------------------------------------------------------------------------

dist = rt.raySegmentIntersect(originPoint, lightRay, a, b) #returns t1 and t2 as tuple

P = a + Point((b - a).x * dist[1], (b - a).y * dist[1])

dirFromIntersectionToPoint = originPoint - P #This is a vector that goes from origin to intersection point in segment

print(P)

dYdX = getDyDx(a, b)
normal = Point(-dYdX.y,dYdX.x) #First normal vector

dot = normal.dot(dirFromIntersectionToPoint)
det = normal.cross(dirFromIntersectionToPoint)
angle = math.atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)



if math.degrees(angle) > 90:
    # wrong angle. recalculate for second normal
    normal = Point(dYdX.y, -dYdX.x)  # second normal
    dot = normal.dot(dirFromIntersectionToPoint)
    det = normal.cross(dirFromIntersectionToPoint)
    angle = math.atan2(det, dot)

    print(math.degrees(angle))
    print(abs(math.degrees(angle)))

if 7 < abs(math.degrees(angle)) < 60:

    lineFromLightToIntersectionPoint = light - P
    dot = normal.dot(lineFromLightToIntersectionPoint)
    det = normal.cross(lineFromLightToIntersectionPoint)
    angleFromLight = math.atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)

    print(math.degrees(angleFromLight))

    if abs(math.degrees(angleFromLight)) < 90:
        print(True)

    else:
        print(False)


else:
    print(False)