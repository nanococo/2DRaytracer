import numpy as np
from PIL import Image

from ICONSTANTS import IConstants
from Point import *


class ImageManager:

    def __init__(self, pReferencePath):

        imageFile = Image.open(pReferencePath)
        self.referenceImage = np.array(imageFile)

        self.imageHeight = len(self.referenceImage)
        self.imageWidth = len(self.referenceImage[0])

        self.resultImage = np.array(Image.new("RGB", (self.imageHeight,  self.imageWidth), (0, 0, 0)))
        #self.resultImage = np.array(Image.new("RGB", (self.imageHeight,  self.imageWidth), (0, 0, 0)))

    def calculatePixelColor(self, length, point, source, light):

        intensity = (1 - (length / 500)) ** 2

        values = (self.referenceImage[int(point.y)][int(point.x)])[:3]

        # combine color, light source and light color
        values = values * intensity * source.light

        return values

    def setPixelColor(self, pPoint, pSources, pColor, lightsOnPoints):
        self.resultImage[int(pPoint.x)][int(pPoint.y)] = pColor // lightsOnPoints