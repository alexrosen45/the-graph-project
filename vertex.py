"""CSC 111 Final Project: Vertex class

Module Description
==================
This module includes our Vertex class. It supports a simple clamping and velocity

Copyright Information
=====================
This file is licensed under the MIT License
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

    def __init__(self, x: float, y: float, randomize: bool = False) -> None:
        self.mass = 5
        if randomize:
            # We use the 1 - random.random() trick to ensure 0 is not a possible value
            # This is because random.random() returns a vlue in the range [0, 1)
            self.x = x + ((1 - random.random()) * 0.02 - 0.01)
            self.y = y + ((1 - random.random()) * 0.02 - 0.01)
        else:
            self.x = x
            self.y = y
        self.vx = 0
        self.vy = 0
        self.pinned = False

    def update(self, friction: float, gravity: float, size: tuple[int, int]) -> float:
        """Update self using graph friction, graph gravity.
        Returns the applied velocity."""
        self.vx *= friction
        self.vy *= friction
        if not self.pinned:
            self.vy += gravity
            self.x += self.vx
            self.y += self.vy
            return (self.vx ** 2 + self.vy ** 2) ** 0.5 if self.y < size[1] else abs(self.vx)
        else:
            return 0.0

    def clamp(self, size: tuple[int, int]) -> None:
        """Clamp self using height and width."""
        width, height = size
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
