import math

from Point import Point
from Segments.Segment import Segment
from VectorialMath.Vectors import getDyDx


class SpecularSegment(Segment):

    def ReflectionConditions(self, origin, lightRay, light, P):
        # dist = rt.raySegmentIntersect(origin, lightRay, self.a, self.b)  # returns t1 and t2 as tuple

        # P = self.a + Point((self.b - self.a).x * dist[1], (self.b - self.a).y * dist[1])

        dirFromIntersectionToPoint = origin - P  # This is a vector that goes from origin to intersection point in segment

        #print(P)

        dYdX = getDyDx(self.a, self.b)
        normal = Point(-dYdX.y, dYdX.x)  # First normal vector

        dot = normal.dot(dirFromIntersectionToPoint)
        det = normal.cross(dirFromIntersectionToPoint)
        angle = math.atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)

        if math.degrees(angle) > 90:
            # wrong angle. recalculate for second normal
            normal = Point(dYdX.y, -dYdX.x)  # second normal
            dot = normal.dot(dirFromIntersectionToPoint)
            det = normal.cross(dirFromIntersectionToPoint)
            angle = math.atan2(det, dot)

            #print(math.degrees(angle))
            #print(abs(math.degrees(angle)))

        if 7 < abs(math.degrees(angle)) < 60:

            lineFromLightToIntersectionPoint = light.point - P
            dot = normal.dot(lineFromLightToIntersectionPoint)
            det = normal.cross(lineFromLightToIntersectionPoint)
            angleFromLight = math.atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)

            #print(math.degrees(angleFromLight))

            if abs(math.degrees(angleFromLight)) < 90 and (math.degrees(angleFromLight)*math.degrees(angle) <= 0):
                #print(True)
                return True

            else:
                #print(False, 1)
                return False

        else:
            #print(False, 2)
            return False



sp = SpecularSegment((1,1,1), Point(11,8), Point(5.2844650363276, 5.7185842823965))