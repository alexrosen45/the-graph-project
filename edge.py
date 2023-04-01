"""
This file holds our Edge class. It includes an initial distance and represent an edge in our graph
"""
import random
from vertex import Vertex

MIN_DISTANCE = 15


class Edge:
    """Massless spring, applies spring forces."""

    initial_distance: float = 5
    start: Vertex
    end: Vertex

    def __init__(self, start: Vertex, end: Vertex, is_random: bool = False) -> None:
        self.start = start
        self.end = end

        # randomize initial_distance
        distance = (self.start.x - self.end.x) ** 2 + (self.start.y - self.end.y) ** 2

        if is_random:
            self.initial_distance = max(
                MIN_DISTANCE, random.uniform(distance - 5, distance + 5) ** 0.5
            )
        else:
            self.initial_distance = max(MIN_DISTANCE, distance**0.5)

    def update(self, fx: float, fy: float) -> None:
        """Update self using fx and fy."""
        self.start.vx -= fx / self.start.mass
        self.start.vy -= fy / self.start.mass
        self.end.vx += fx / self.end.mass
        self.end.vy += fy / self.end.mass


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(
        config={
            "extra-imports": ["vertex", "random"],
            "allowed-io": [],
            "max-line-length": 100,
        }
    )
 