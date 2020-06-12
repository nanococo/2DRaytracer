from abc import abstractmethod

class Geometry:
    arrayOfPoints = []

    @abstractmethod
    def calculateReflection(self):
        pass