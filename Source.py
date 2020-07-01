import numpy as np

from ICONSTANTS import IConstants

class Source:

    def __init__(self, pPoint, pColor, pImageHeight, pImageWidth, pIntensity):

        self.light = np.array(pColor)
        self.point = pPoint
        self.rangeAreas = []
        self.setRangeAreasList(pImageHeight, pImageWidth)
        self.rangeQuantity = len(self.rangeAreas)
        self.intensity = pIntensity



    # Sets rangeAreas attribute.
    def setRangeAreasList(self, pImageHeight, pImageWidth):

        sourceRange = IConstants.INITIAL_LIGHT_RANGE

        while sourceRange < pImageWidth and sourceRange < pImageHeight:

            sourceRangeX = list(self.setSourceRange(self.point.x, sourceRange, pImageWidth))
            sourceRangeY = list(self.setSourceRange(self.point.y, sourceRange, pImageHeight))

            sourceArea = [sourceRangeX, sourceRangeY]

            self.rangeAreas += [sourceArea]

            sourceRange += IConstants.LIGHT_RANGE_EXPANSION_RATE



    # Sets the random source range, to prevent it from going out of index in expansion.
    def setSourceRange(self, sourcePositionValue, pSourceRange, pUpperLimit):

        # sourcePositionValue is source.x or source.y
        # upperLimit is the Image Height or Width

        rangeBegin = sourcePositionValue - pSourceRange
        rangeEnd = sourcePositionValue + pSourceRange

        if rangeBegin < 0:
            rangeBegin = 0

        if rangeEnd > pUpperLimit:
            rangeEnd = pUpperLimit

        return range(rangeBegin, rangeEnd)
