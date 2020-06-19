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
from Source import Source
import math

imageManager = ImageManager("fondo.png")
sources = [
           #Source(Point(195, 200), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth),
           Source(Point(294, 200), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth),
           #Source(Point(94, 200), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth),
           #Source(Point(394, 200), [1, 1, 1], imageManager.imageHeight, imageManager.imageWidth)
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
    sourceAreasIndex = 0
    nonSourceProbability = IConstants.INITIAL_NON_SOURCE_PROBABILITY

    while True:

        # random point in the image
        point = directedRandomPoint(sourceAreasIndex, nonSourceProbability, sources)
        lightsOnPoint = 1
        # point = Point(random.uniform(0,500), random.uniform(0,500))

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

            #---------------------------------------DIRECT LIGHTING--------------------------------------------
            free = True
            for seg in segments:

                # check if ray intersects with segment
                dist = rt.raySegmentIntersect(point, dir, seg[0], seg[1])
                # if intersection, or if intersection is closer than light source
                if 0 < dist[0] < length2:
                    free = False
                    break

            if free:
                # call imageManager method for color calculation
                pixel += imageManager.calculatePixelColor(length, point, source, light)
                lightsOnPoint+=1

            # -------------------------------------INDIRECT LIGHTING--------------------------------------------
            # (GLOBAL ILLUMINATION PROCESS HERE)

            #FIRST: Add a vector to every 45 degrees from reference point
                #USES:  Base light ray vector BASE_VECTOR_LENGTH. Rotates from this
                #       Origin set by reference point

            raysFromPoint = [] # <- Array of vectors (Points) that define directions and range for light rays. Origin is the point
            origin = (point.x, point.y) #Since point is of type Point, convert its values to a single tuple
            angle = 0 #Initial value of 45. Increments by 45 each loop
            for i in range(8):
                rotatedTuple = rotate(origin, (IConstants.BASE_VECTOR_RAY.x, IConstants.BASE_VECTOR_RAY.y), math.radians(angle)) #Returns a rotated vector by n-degree as tuple
                raysFromPoint.append(Point(rotatedTuple[0], rotatedTuple[1])) #Created new Point from rotated vector-tuple
                angle+=45

            #SECOND: Iterate each ray to see if it intersects with a segment. Might intersect with multiple segments since
            #        it goes in 360 degrees each 45th degree (Star like pattern)
            #       Each ray will be iterated with all segments present

            for ray in raysFromPoint: #Each ray is a vector represented by a Point
                for seg in segments:

                    A = seg[0] #Segment point A
                    B = seg[1] #Segment point B
                    dist = rt.raySegmentIntersect(point, ray, seg[0], seg[1])

                    if 0 < dist[0] < IConstants.BASE_VECTOR_RAY_LENGTH_NORMALIZED:
                        #(THIS MEANS BOUNCE SINCE IT INTERSECTS!!!)

                        # THIRD: Calculate intersection point with segment.
                        P = A + Point((B - A).x * dist[1], (B - A).y * dist[1]) # <- Return a Point type value
                        firstRayVector = P - point #Defines a vector between the point and the intersection point P
                        firstLength = rt.length(firstRayVector) #Length of such vector

                        #FOURTH: Calculate direct lighting from new point to source value. If no other
                        #        Intersection is found, the is a valid indirect lighting

                        #--------------------------------SECOND DIRECT LIGHTING -------------------------------
                        dir2 = source.point - P #Direction vector between source and new Point P

                        secondLength = rt.length(dir2) #distance between Point P and light source
                        secondLength2 = rt.length(rt.normalize(dir2)) # normalized distance to source

                        free2 = True
                        for seg2 in segments:

                            # check if ray intersects with segment
                            dist2 = rt.raySegmentIntersect(P, dir2, seg2[0], seg2[1])
                            # if intersection, or if intersection is closer than light source
                            if 0 < dist2[0] < secondLength2:
                                free2 = False
                                break

                        if free2:
                            # call imageManager method for color calculation
                            pixel += imageManager.calculatePixelColor(firstLength+secondLength, point, source, light)
                            lightsOnPoint += 1

                        break


            # average pixel value and assign
            imageManager.setPixelColor(point, sources, pixel, lightsOnPoint)

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