import random
import threading
import time

import numpy as np
import pygame
from numpy.ma import arange

import rt
from ICONSTANTS import IConstants
from ImageManager import ImageManager
from Point import *
from Segment import Segment
from Source import Source
import math

imageManager = ImageManager("fondoB.png")
sources = [
           Source(Point(27, 25), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth, 1),
           Source(Point(204, 25), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth, 1),
           Source(Point(40, 226), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth, 1),
           Source(Point(270, 257), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth, 1),
           Source(Point(417, 88), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth, 1),
           Source(Point(483, 145), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth, 1),
          ]



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


def raytrace():
    # Raytraces the scene progressively

    timerStart = time.time()
    totalTime = time.time()
    sourceAreasIndex = 0
    nonSourceProbability = IConstants.INITIAL_NON_SOURCE_PROBABILITY

    while True:

        # random point in the image
        try:

            point = directedRandomPoint(sourceAreasIndex, nonSourceProbability, sources)

        except IndexError:
            totalTimeStop = time.time() - totalTime
            print(totalTimeStop)

        lightsOnPoint = 0
        #point = Point(random.uniform(0, imageManager.imageWidth),
                     # random.uniform(0, imageManager.imageHeight))

        # pixel color
        pixel = 0

        for source in sources:

            # calculates direction to light source

            dir = source.point - point
            if dir.x == 0 and dir.y == 0:
                continue

            # distance between point and light source
            length = rt.length(dir)

            # normalized distance to source
            length2 = rt.length(rt.normalize(dir))

            free = True
            for seg in segments:

                # check if ray intersects with segment
                dist = rt.raySegmentIntersect(point, dir, seg.PointA, seg.PointB)
                # if intersection, or if intersection is closer than light source
                if 0 < dist[0] < length2:
                    free = False
                    break

            if free:
                # call imageManager method for color calculation
                pixel += imageManager.calculatePixelColor(length, point, source)
                lightsOnPoint += 1


        # average pixel value and assign
        imageManager.setPixelColor(point, pixel, lightsOnPoint)

        timerEnd = time.time()
        if (timerEnd - timerStart) % IConstants.SECONDS_BEFORE_CHANGE:
            timerStart = time.time()
            sourceAreasIndex += 1
            if sourceAreasIndex == sources[0].rangeQuantity:  # prevent the source areas index from going out of range
                sourceAreasIndex -= 1
            nonSourceProbability += IConstants.NON_SOURCE_PROBABILITY_INCREASE


# returns a point elected with a directed random.
def directedRandomPoint(sourceAreasIndex, nonSourceProbability, sourcesList):
    """
    # Chooses between full random or random between source ranges
    segmentChoice = random.uniform(0, 100)

    if segmentChoice < nonSourceProbability:

        # Selects a full random
        x = random.choice(arange(0, imageManager.imageWidth))
        y = random.choice(arange(0, imageManager.imageHeight))
        return Point(x, y)

    else:

        # Selects a random index choice between the lists of source ranges
        sourceRangeChoice = random.choice(arange(0, len(sourcesList)))

        # Selects a random X and Y in the chosen source range and pops the choice from the list

        xChoicePool = sourcesList[sourceRangeChoice].rangeAreas[sourceAreasIndex][0]
        x = random.choice(xChoicePool)
        #xIndex = xChoicePool.index(x)
        #xChoicePool.pop(xIndex)

        yChoicePool = sourcesList[sourceRangeChoice].rangeAreas[sourceAreasIndex][1]
        y = random.choice(yChoicePool)
        #yIndex = yChoicePool.index(y)
        #yChoicePool.pop(yIndex)
        """

    choices = imageManager.pixelPointsPool

    choiceIndex = random.choice(arange(0, len(choices)))

    x = choices[choiceIndex][0]
    y = choices[choiceIndex][1]

    choices.pop(choiceIndex)

    return Point(x, y)


def getFrame():
    # grabs the current image and returns it
    return imageManager.resultImage


# pygame stuff
h, w = imageManager.imageHeight, imageManager.imageWidth

border = 50
pygame.init()

screen = pygame.display.set_mode((w + (2 * border), h + (2 * border)))

pygame.display.set_caption("2D Raytracing")
done = False
clock = pygame.time.Clock()

# init random
random.seed()

# light positions
#sources = [Point(195, 200), Point(294, 200)]

# light color
light = np.array([1, 1, 0.75])
# light = np.array([1, 1, 1])

# warning, point order affects intersection test!!
segments = [

    # Room segments
    Segment([1, 1, 1], Point(350, 0), Point(350, 180)),
    Segment([1, 1, 1], Point(350, 239), Point(350, imageManager.imageHeight)),
    Segment([1, 1, 1], Point(350, 239), Point(358, 239)),
    Segment([1, 1, 1], Point(358, 239), Point(358, imageManager.imageHeight)),
    Segment([1, 1, 1], Point(394, 239), Point(394, imageManager.imageHeight)),
    Segment([1, 1, 1], Point(394, 239), Point(imageManager.imageWidth, 239)),
    Segment([1, 1, 1], Point(350, 180), Point(409, 180)),
    Segment([1, 1, 1], Point(409, 171), Point(409, 180)),
    Segment([1, 1, 1], Point(449, 180), Point(imageManager.imageWidth, 180)),
    Segment([1, 1, 1], Point(449, 171), Point(449, 180)),

    # Bathroom walls
    Segment([1, 1, 1], Point(360, 0), Point(360, 171)),
    Segment([1, 1, 1], Point(360, 171), Point(409, 171)),
    Segment([1, 1, 1], Point(449, 171), Point(452, 171)),
    Segment([1, 1, 1], Point(452, 111), Point(452, 127)),
    Segment([1, 1, 1], Point(452, 162), Point(452, 171)),
    Segment([1, 1, 1], Point(452, 127), Point(441, 161)),
    Segment([1, 1, 1], Point(452, 111), Point(477, 111)),
    Segment([1, 1, 1], Point(477, 102), Point(477, 111)),
    Segment([1, 1, 1], Point(477, 102), Point(imageManager.imageWidth, 102)),

    # Toilet part
    Segment([1, 1, 1], Point(452, 127), Point(460, 127)),
    Segment([1, 1, 1], Point(452, 162), Point(460, 162)),
    Segment([1, 1, 1], Point(460, 119), Point(460, 127)),
    Segment([1, 1, 1], Point(460, 162), Point(460, 171)),
    Segment([1, 1, 1], Point(460, 119), Point(imageManager.imageWidth, 119)),
    Segment([1, 1, 1],  Point(460, 171), Point(imageManager.imageWidth, 171)),


]

# thread setup
t = threading.Thread(target=raytrace)  # f being the function that tells how the ball should move
t.setDaemon(True)  # Alternatively, you can use "t.daemon = True"
t.start()

# main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Clear screen to white before drawing
    screen.fill((255, 255, 255))

    # Get a numpy array to display from the simulation
    npimage = getFrame()

    # Convert to a surface and splat onto screen offset by border width and height
    surface = pygame.surfarray.make_surface(npimage)
    screen.blit(surface, (border, border))

    pygame.display.flip()
    clock.tick(60)