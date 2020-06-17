from ICONSTANTS import IConstants
import numpy as np
import pygame
import random
from random import choices
from PIL import Image
from numpy.ma import arange
from itertools import chain
from Source import Source
from ImageManager import ImageManager
from Point import *
import rt
import math
import threading
import time

imageManager = ImageManager("fondo.png")
sources = [
           Source(Point(195, 200), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth),
           Source(Point(294, 200), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth),
           #Source(Point(94, 200), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth),
           #Source(Point(394, 200), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth)
          ]


def raytrace():
    # Raytraces the scene progessively

    timerStart = time.time()
    sourceAreasIndex = 0
    nonSourceProbability = IConstants.INITIAL_NON_SOURCE_PROBABILITY

    while True:

        # random point in the image
        point = directedRandomPoint(sourceAreasIndex, nonSourceProbability, sources)
        # point = Point(random.uniform(0,500), random.uniform(0,500))

        # pixel color
        pixel = 0

        for source in sources:

            # calculates direction to light source

            dir = source.point - point
            if dir.x == 0 and dir.y == 0:
                continue
            # add jitter

            # distance between point and light source
            length = rt.length(dir)

            # normalized distance to source
            length2 = rt.length(rt.normalize(dir))

            free = True
            for seg in segments:  # Este es el ciclo que cambia con la iluminación global
                # check if ray intersects with segment
                dist = rt.raySegmentIntersect(point, dir, seg[0], seg[1])
                # if intersection, or if intersection is closer than light source
                if 0 < dist < length2:
                    free = False
                    break

            if free:
                # call imageManager method for color calculation
                pixel += imageManager.calculatePixelColor(length, point, source, light)

            # average pixel value and assign
            imageManager.setPixelColor(point, sources, pixel)

        timerEnd = time.time()
        if (timerEnd - timerStart) > IConstants.SECONDS_BEFORE_CHANGE:
            timerStart = time.time()
            sourceAreasIndex += 1
            if sourceAreasIndex == sources[0].rangeQuantity:  # prevent the source areas index from going out of range
                sourceAreasIndex -= 1
            nonSourceProbability += IConstants.NON_SOURCE_PROBABILITY_INCREASE


# returns a point elected with a directed random.
def directedRandomPoint(sourceAreasIndex, nonSourceProbability, sourcesList):

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

        # Selects a random X and Y in the chosen source range
        x = random.choice(sourcesList[sourceRangeChoice].rangeAreas[sourceAreasIndex][0])
        y = random.choice(sourcesList[sourceRangeChoice].rangeAreas[sourceAreasIndex][1])

        return Point(x, y)


def getFrame():
    # grabs the current image and returns it
    return imageManager.resultImage


# pygame stuff
h, w = 550, 550
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
    ([Point(180, 135), Point(215, 135)]),
    ([Point(285, 135), Point(320, 135)]),
    ([Point(320, 135), Point(320, 280)]),
    ([Point(320, 320), Point(320, 355)]),
    ([Point(320, 355), Point(215, 355)]),
    ([Point(180, 390), Point(180, 286)]),
    ([Point(180, 286), Point(140, 286)]),
    ([Point(320, 320), Point(360, 320)]),
    ([Point(180, 250), Point(180, 135)]),
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







