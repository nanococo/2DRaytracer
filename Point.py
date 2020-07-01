class Point:

    x = 0.0
    y = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isLightAtEnd = False
        self.lightIndex = -1

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)   

    def __truediv__(self, other):
        return Point(self.x/other, self.y/other)

    def __mul__(self, other):
        #Mul from a scalar value
        return Point(self.x*other, self.y*other)

    def dot(self, p2):
        return (self.x*p2.x) + (self.y*p2.y)

    def cross(self, p2):
        return (self.x*p2.y) - (self.y*p2.x)

    def __str__(self):
        return "[ {}, {}]".format(self.x, self.y)