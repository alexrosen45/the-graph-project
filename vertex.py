"""
This module includes our Vertex class. It supports a simple clamping and velocity
"""
import random


class Vertex:
    """Vertex class that stores a mass in a system of springs."""

    mass: float
    x: float
    y: float
    vx: float
    vy: float
    pinned: bool

    def __init__(self, x: float, y: float) -> None:
        self.mass = 5
        # We use the 1 - random.random() trick to ensure 0 is not a possible value
        # This is because random.random() returns a vlue in the range [0, 1)
        self.x = x + ((1 - random.random()) * 0.02 - 0.01)
        self.y = y + ((1 - random.random()) * 0.02 - 0.01)
        self.vx = 0
        self.vy = 0
        self.pinned = False

    def update(self, friction: float, gravity: float, dt: float) -> None:
        """Update self using graph friction, graph gravity, and time change."""
        self.vx *= 1 - (friction * dt)
        self.vy *= 1 - (friction * dt)
        self.vy += gravity * dt
        if not self.pinned:
            self.x += self.vx * dt
            self.y += self.vy * dt

    def clamp(self, height: int, width: int) -> None:
        """Clamp self using height and width."""
        if not self.pinned:
            self.y = min(self.y, height)
            self.x = max(min(self.x, width), 0)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(
        config={
            "extra-imports": ["random"],
            "allowed-io": [],
            "max-line-length": 100,
        }
    )
