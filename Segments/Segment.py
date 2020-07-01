from abc import abstractmethod


class Segment:

    def __init__(self, pColor, pPointA, pPointB):
        self.a = pPointA  # Point object
        self.b = pPointB  # Point object
        self.Color = pColor  # RGB, 0 to 1 representation

    @abstractmethod
    def ReflectionConditions(self, origin, lightRay, light, P):  # Returns true if reflection conditions are met
        ...

    def CalculateReflectionIntensity(self):  # Returns a 0 to 1 value on the intensity of the pixel affected by
                                             # indirect light
        ...
