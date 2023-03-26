import random


class Vertex:
    """Vertex class that stores a mass in a system of springs."""
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

    def update(self, friction: float, gravity: float, dt: float):
        """Update self using graph friction, graph gravity, and time change."""
        self.vx *= (1 - (friction * dt))
        self.vy *= (1 - (friction * dt))
        self.vy += gravity * dt
        if not self.pinned:
            self.x += (self.vx * dt)
            self.y += (self.vy * dt)

    def clamp(self, height: int, width: int) -> None:
        """Clamp self using height and width."""
        if not self.pinned:
            self.y = min(self.y, height)
            self.x = max(min(self.x, width), 0)
