from ICONSTANTS import IConstants
import numpy as np
import pygame
import random
from random import choices
from PIL import Image
from numpy.ma import arange
from itertools import chain
from Point import *
import rt
import math
import threading

 

def raytrace():
    #Raytraces the scene progessively

    lightRange = IConstants.INITIAL_LIGHT_RANGE
    lightRangeCounter = 0
    sourceAreasList = setSourceAreasList(lightRange)
    nonSourceProbability = IConstants.NON_SOURCE_PROBABILITY

    while True:

        #random point in the image
        point = directedRandomPoint(lightRange, sourceAreasList)

        #point = Point(random.uniform(0,500), random.uniform(0,500))

        #pixel color
        pixel = 0

        for source in sources:

            #calculates direction to light source

            dir = source-point
            if dir.x == 0 and dir.y == 0:
                continue
            #add jitter
            #dir.x += random.uniform(0, 25)
            #dir.y += random.uniform(0, 25)

            #distance between point and light source
            length = rt.length(dir)
            #normalized distance to source
            length2 = rt.length(rt.normalize(dir))
            
            free = True
            for seg in segments:                
                #check if ray intersects with segment
                dist = rt.raySegmentIntersect(point, dir, seg[0], seg[1])
                #if intersection, or if intersection is closer than light source
                if  dist > 0 and length2>dist:
                    free = False
                    break

            if free:        
                intensity = (1-(length/500))**2
                #print(len)
                #intensity = max(0, min(intensity, 255))
                values = (ref[int(point.y)][int(point.x)])[:3]
                #combine color, light source and light color
                values = values * intensity * light
                
                #add all light sources 
                pixel += values
            
            #average pixel value and assign
            px[int(point.x)][int(point.y)] = pixel // len(sources)

        lightRangeCounter += 1
        if lightRangeCounter % 10 ** 5 == 0:
            lightRange += 50
            sourceAreasList = setSourceAreasList(lightRange)
            nonSourceProbability += 20






# returns a point elected with a directed random.
def directedRandomPoint(lightRange, sourceAreasList):

    # Chooses between full random or random between source ranges
    segmentChoice = random.uniform(0, 100)

    if segmentChoice < IConstants.NON_SOURCE_PROBABILITY:
        # Selects a full random
        x = random.choice(arange(0, IConstants.IMAGE_WIDTH))
        y = random.choice(arange(0, IConstants.IMAGE_HEIGHT))
        return Point(x, y)
    else:
        # Selects a random index choice between the lists of source ranges
        sourceRangeChoice = random.choice(arange(0, len(sourceAreasList)))
        # Selects a random X and Y in the chosen source range
        x = random.choice(sourceAreasList[sourceRangeChoice][0])
        y = random.choice(sourceAreasList[sourceRangeChoice][1])

        return Point(x, y)


# returns a list with the format: [[[sourceXRange], [sourceYRange]], [[sourceXRange], [sourceYRange]], ... ]
def setSourceAreasList(lightRange):

    sourceAreasList = []
    # Each index is a source range divided by two other lists that represent the options on X and the options of Y

    for source in sources:

        sourceRangeX = list(setSourceRange(source.x, lightRange, IConstants.IMAGE_WIDTH))
        sourceRangeY = list(setSourceRange(source.y, lightRange, IConstants.IMAGE_HEIGHT))
        sourceRange = [sourceRangeX, sourceRangeY]
        sourceAreasList += [sourceRange]

    return sourceAreasList


# Sets the random source range, to prevent it from going out of index in expansion.
def setSourceRange(sourcePositionValue, lightRange, upperLimit):
    # sourcePositionValue is source.x or source.y
    # upperLimit is the Image Height or Width
    rangeBegin = sourcePositionValue - lightRange
    rangeEnd = sourcePositionValue + lightRange
    if rangeBegin < 0:
        rangeBegin = 0
    if rangeEnd > upperLimit:
        rangeEnd = upperLimit
    return range(rangeBegin, rangeEnd)



def getFrame():
    # grabs the current image and returns it
    #pixels = np.roll(px,(1,2),(0,1))
    pixels = px
    return pixels


#pygame stuff
h,w=550,550
border=50
pygame.init()
screen = pygame.display.set_mode((w+(2*border), h+(2*border)))
pygame.display.set_caption("2D Raytracing")
done = False
clock = pygame.time.Clock()

#init random
random.seed()

#image setup
i = Image.new("RGB", (500, 500), (0, 0, 0))
px = np.array(i)

#reference image for background color
im_file = Image.open("fondo.png")
ref = np.array(im_file)

#light positions
sources = [ Point(195, 200), Point( 294, 200) ]

#light color
light = np.array([1, 1, 0.75])
#light = np.array([1, 1, 1])

#warning, point order affects intersection test!!
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



#thread setup
t = threading.Thread(target = raytrace) # f being the function that tells how the ball should move
t.setDaemon(True) # Alternatively, you can use "t.daemon = True"
t.start()

#main loop
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

        # Clear screen to white before drawing 
        screen.fill((255, 255, 255))

        # Get a numpy array to display from the simulation
        npimage=getFrame()

        # Convert to a surface and splat onto screen offset by border width and height
        surface = pygame.surfarray.make_surface(npimage)
        screen.blit(surface, (border, border))

        pygame.display.flip()
        #clock.tick(60)







