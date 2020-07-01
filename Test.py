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



p = rotate((4,8), (10, 8), math.radians(-45))
print(p)

O = Point(4,8)
P = Point(p[0], p[1])

direction = P-O
print(direction)

length2Ray = rt.length(rt.normalize(direction))

A = Point(6,2)
B = Point(8,6)
dist = rt.raySegmentIntersect(O, direction, A, B)

if 0 < dist[0] < length2Ray:
    P = A + Point((B - A).x * dist[1], (B - A).y * dist[1])
    dirFromIntersectionToPoint = O - P
    dirFromPointToIntersection = P - O
    print(dirFromIntersectionToPoint)

    dYdX = getDyDx(A, B)
    normal = Point(-dYdX.y,dYdX.x)

    dot = normal.dot(dirFromIntersectionToPoint)
    det = normal.cross(dirFromIntersectionToPoint)
    angle = math.atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)

    if angle > 90:
        #wrong angle. recalculate for second normal
        normal = Point(dYdX.y, -dYdX.x) #second normal
        dot = normal.dot(dirFromIntersectionToPoint)
        det = normal.cross(dirFromIntersectionToPoint)
        angle = math.atan2(det, dot)
    print(abs(math.degrees(angle)))

    fV = dirFromPointToIntersection - (normal*( 2 * ( dirFromPointToIntersection.dot(normal) / normal.dot(normal) ) ))
    print(fV)

#print(getAngle((8.2426406871193,3.7573593128807), (4, 8), (10, 8)))