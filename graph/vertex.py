class Vertex:
    """
    Vertex class that stores a mass in a system of springs
    """
    mass: float
    x: float
    y: float
    vx: float
    vy: float

    def __init__(self, x, y):
        self.mass = 5
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
