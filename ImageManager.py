import numpy as np
from PIL import Image

from ICONSTANTS import IConstants
from Point import *


class ImageManager:

    def __init__(self, pReferencePath):

        imageFile = Image.open(pReferencePath)
        width, height = imageFile.size
        self.referenceImage = np.array(imageFile)

        self.imageHeight = height
        self.imageWidth = width

        self.resultImage = np.array(Image.new("RGB", (self.imageHeight,  self.imageWidth), (0, 0, 0)))
        #self.resultImage = np.array(Image.new("RGB", (self.imageHeight,  self.imageWidth), (0, 0, 0)))

        self.pixelPointsPool = self.setPixelPointsPool(self.imageHeight, self.imageWidth)

    def calculatePixelColor(self, length, point, source):

        intensity = (source.intensity - (length / 500)) ** 2
        values = (self.referenceImage[int(point.y)][int(point.x)])[:3]

        # combine color, light source and light color
        values = values * intensity * source.light

        return values

    def setPixelPointsPool(self, pImageHeight, pImageWidth):

        result = []
        for xCoordinate in range(0, pImageWidth):
            for yCoordinate in range(0, pImageHeight):
                result += [[xCoordinate, yCoordinate]]

        return result

    def setPixelColor(self, pPoint, pColor, lightsOnPoints):
        try:
            #print(pColor)
            self.resultImage[int(pPoint.x)][int(pPoint.y)] = pColor // 4
        except ZeroDivisionError:
            self.resultImage[int(pPoint.x)][int(pPoint.y)] = pColor // 1

