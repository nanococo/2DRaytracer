import math
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
from Segments.NonSpecularSegment import NonSpecularSegment
from Segments.SpecularSegment import SpecularSegment
from Source import Source
from VectorialMath.Vectors import rotate

imageManager = ImageManager("fondoB.png")
sources = [
           Source(Point(27, 25), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth, 1),
           #Source(Point(204, 25), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth, 1),
           Source(Point(40, 226), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth, 1),
           #Source(Point(270, 257), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth, 1),
           #Source(Point(417, 88), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth, 1),
           Source(Point(483, 145), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth, 1),
          ]


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
            break

        lightsOnPoint = 0
        #point = Point(random.uniform(0, imageManager.imageWidth),
                     # random.uniform(0, imageManager.imageHeight))

        # pixel color
        pixel = 0

        rays = initRays(point, sources)
        for ray in rays:
            pixel += directLight(point, ray) # Pending calculation on lights on point


        # average pixel value and assign
        imageManager.setPixelColor(point, pixel, lightsOnPoint)

        timerEnd = time.time()
        if (timerEnd - timerStart) % IConstants.SECONDS_BEFORE_CHANGE:
            timerStart = time.time()
            sourceAreasIndex += 1
            if sourceAreasIndex == sources[0].rangeQuantity:  # prevent the source areas index from going out of range
                sourceAreasIndex -= 1
            nonSourceProbability += IConstants.NON_SOURCE_PROBABILITY_INCREASE


def initRays(point, sources):
    rays = []
    for i in range(0, 8):
        pointAtEndOfRay = Point(point.x + IConstants.BASE_VECTOR_RAY.x, point.y)
        rotatedPoint = rotate((point.x, point.y), (pointAtEndOfRay.x, pointAtEndOfRay.y), math.radians(-45))
        rays.append(Point(rotatedPoint[0], rotatedPoint[1]) - point)
    for source in sources:
        dir = source.point - point
        dir.isLightAtEnd = True
        dir.lightIndex = sources.index(source)
        rays.append(dir)
    return rays

def directLight(point, ray):

    if ray.x == 0 and ray.y == 0:
        return 0
    # distance between point and light source
    length = rt.length(ray)
    # normalized distance to source
    length2 = rt.length(rt.normalize(ray))
    free = True
    for segment in segments:
        # check if ray intersects with segment
        dist = rt.raySegmentIntersect(point, ray, segment.a, segment.b)
        # if intersection, or if intersection is closer than light source
        if 0 < dist[0] < length2:
            # Direct ray had intersection
            P = segment.a + Point((segment.b - segment.a).x * dist[1], (segment.b - segment.a).y * dist[1])
            indirectLighting = rebound(point, ray, P, segment)
            if not isinstance(indirectLighting, int):
               return indirectLighting
            free = False

    if free and ray.isLightAtEnd:
        return imageManager.calculatePixelColor(length, point, sources[ray.lightIndex])
    else:
        return 0

def rebound(originPoint, ray, intersectionPoint, segment):
    """
    :param originPoint:
    :param newPoint:
    :param segment:
    :return: an imageManager.calculatePixelColor if indirect light is reached, 0 otherwise
    """
    #print("Rebound")
    pixel = 0

    for i in range(0, len(sources)):
        #print(i)
        if segment.ReflectionConditions(originPoint, ray, sources[i], intersectionPoint):  # if vectorial conditions are met
            #print("Valid Reflection")
            direction = sources[i].point - intersectionPoint
            length = rt.length(direction)
            length2 = rt.length(rt.normalize(direction))
            free = True
            for seg in segments:
                if seg == segment:
                    continue
                distance = rt.raySegmentIntersect(intersectionPoint, direction, seg.a, seg.b)
                if 0 < distance[0] < length2:
                    free = False
            if free:
                colorBleeding = calculateColorBleeding(sources[i], length, segment.Color, intersectionPoint)
                originLength = rt.length(originPoint)
                pixel += imageManager.calculatePixelColor(originLength, originPoint, colorBleeding)
        else:
            continue

    return pixel

def calculateColorBleeding(pSource, pLength, pSegmentColor, pIntersectionPoint):
    newColor = [(pSource.light[0] + pSegmentColor[0]) // 2,
                (pSource.light[1] + pSegmentColor[1]) // 2,
                (pSource.light[2] + pSegmentColor[2]) // 2]
    intensityDecrementation = random.uniform(0, 5)
    newIntensity = 0.01
    #print("Color Bleeding")
    #print(pIntersectionPoint, newColor, imageManager.imageHeight, imageManager.imageWidth, newIntensity)
    return Source(pIntersectionPoint, newColor, imageManager.imageHeight, imageManager.imageWidth, newIntensity)



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

        # Selects a random X and Y in the chosen source range and pops the choice from the list

        xChoicePool = sourcesList[sourceRangeChoice].rangeAreas[sourceAreasIndex][0]
        x = random.choice(xChoicePool)
        #xIndex = xChoicePool.index(x)
        #xChoicePool.pop(xIndex)

        yChoicePool = sourcesList[sourceRangeChoice].rangeAreas[sourceAreasIndex][1]
        y = random.choice(yChoicePool)
        #yIndex = yChoicePool.index(y)
        #yChoicePool.pop(yIndex)


    # choices = imageManager.pixelPointsPool
    #
    # choiceIndex = random.choice(arange(0, len(choices)))
    #
    # x = choices[choiceIndex][0]
    # y = choices[choiceIndex][1]
    #
    # choices.pop(choiceIndex)

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

    SpecularSegment([1, 1, 1], Point(0, 0), Point(imageManager.imageWidth, 0)),
    SpecularSegment([1, 1, 1], Point(0, 0), Point(0, imageManager.imageHeight)),
    SpecularSegment([1, 1, 1], Point(0, imageManager.imageHeight), Point(imageManager.imageWidth, imageManager.imageHeight)),
    SpecularSegment([1, 1, 1], Point(imageManager.imageWidth, 0), Point(imageManager.imageWidth, imageManager.imageHeight)),

    # NonSpecularSegment([1, 1, 1], Point(0, 199), Point(79, 199)),
    # NonSpecularSegment([1, 1, 1], Point(79, 199), Point(79, imageManager.imageHeight)),
    #
    # NonSpecularSegment([1, 1, 1], Point(0, 60), Point(61, 60)),
    # NonSpecularSegment([1, 1, 1], Point(61, 0), Point(61, 60)),

    # Room segments
    SpecularSegment([1, 0, 0], Point(350, 0), Point(350, 180)),
    SpecularSegment([0, 1, 0], Point(350, 239), Point(350, imageManager.imageHeight)),
    SpecularSegment([0, 0, 1], Point(350, 239), Point(358, 239)),
    SpecularSegment([1, 1, 1], Point(358, 239), Point(358, imageManager.imageHeight)),
    SpecularSegment([1, 1, 1], Point(394, 239), Point(394, imageManager.imageHeight)),
    SpecularSegment([1, 1, 1], Point(394, 239), Point(imageManager.imageWidth, 239)),
    SpecularSegment([1, 1, 1], Point(350, 180), Point(409, 180)),
    SpecularSegment([1, 1, 1], Point(409, 171), Point(409, 180)),
    SpecularSegment([1, 1, 1], Point(449, 180), Point(imageManager.imageWidth, 180)),
    SpecularSegment([1, 1, 1], Point(449, 171), Point(449, 180)),

    # Bathroom walls
    SpecularSegment([1, 1, 1], Point(360, 0), Point(360, 171)),
    SpecularSegment([1, 1, 1], Point(360, 171), Point(409, 171)),
    SpecularSegment([1, 1, 1], Point(449, 171), Point(452, 171)),
    SpecularSegment([1, 1, 1], Point(452, 111), Point(452, 127)),
    SpecularSegment([1, 1, 1], Point(452, 162), Point(452, 171)),
    SpecularSegment([1, 1, 1], Point(452, 127), Point(441, 161)),
    SpecularSegment([1, 1, 1], Point(452, 111), Point(477, 111)),
    SpecularSegment([1, 1, 1], Point(477, 102), Point(477, 111)),
    SpecularSegment([1, 1, 1], Point(477, 102), Point(imageManager.imageWidth, 102)),

    # Toilet part
    SpecularSegment([1, 1, 1], Point(452, 127), Point(460, 127)),
    SpecularSegment([1, 1, 1], Point(452, 162), Point(460, 162)),
    SpecularSegment([1, 1, 1], Point(460, 119), Point(460, 127)),
    SpecularSegment([1, 1, 1], Point(460, 162), Point(460, 171)),
    SpecularSegment([1, 1, 1], Point(460, 119), Point(imageManager.imageWidth, 119)),
    SpecularSegment([1, 1, 1],  Point(460, 171), Point(imageManager.imageWidth, 171)),


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