import random


class Vertex:
    """
    Vertex class that stores a mass in a system of springs
    """
    mass: float
    x: float
    y: float
    vx: float
    vy: float
    pinned: bool

    def __init__(self, x, y):
        self.mass = 5
        self.x = x + ((1-random.random())*0.02-0.01)
        self.y = y + ((1-random.random())*0.02-0.01)
        self.vx = 0
        self.vy = 0
        self.pinned = False
