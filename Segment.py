from abc import abstractmethod


class Segment:

    def __init__(self, pColor, pPointA, pPointB):
        self.PointA = pPointA  # Point object
        self.PointB = pPointB  # Point object
        self.Color = pColor  # RGB, 0 to 1 representation

    @abstractmethod
    def ReflectionConditions(self):  # Returns true if reflection conditions are met
        ...

    def CalculateReflectionIntensity(self):  # Returns a 0 to 1 value on the intensity of the pixel affected by
                                             # indirect light
        ...
