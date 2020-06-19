import rt
from Point import Point


class IConstants:  # "Interface" that contains all constant values to prevent hard code

    INITIAL_LIGHT_RANGE = 100
    LIGHT_RANGE_EXPANSION_RATE = 50
    INITIAL_NON_SOURCE_PROBABILITY = 10
    NON_SOURCE_PROBABILITY_INCREASE = 20
    SECONDS_BEFORE_CHANGE = 15

    BASE_VECTOR_RAY = Point(0, 200)
    BASE_VECTOR_RAY_LENGTH = rt.length(BASE_VECTOR_RAY)
    BASE_VECTOR_RAY_LENGTH_NORMALIZED = rt.length(rt.normalize(BASE_VECTOR_RAY))


