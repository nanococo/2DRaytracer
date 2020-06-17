from abc import abstractmethod


class Geometry:

    points = ()

    def __init__(self, pPointA, pPointB):
        self.points = (pPointA, pPointB)

    @abstractmethod
    def calculateReflection(self):
        pass



