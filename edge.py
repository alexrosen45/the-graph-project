"""CSC 111 Final Project: Edge Class

Module Description
==================
This file holds our Edge class. It includes an initial distance and represent an edge in our graph

Copyright Information
=====================
This file is licensed under the MIT License
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
        if self.start.pinned and self.end.pinned:
            return

        start_multiplier = 1 if self.end.pinned else 0.5
        end_multiplier = 1 if self.start.pinned else 0.5
        self.start.vx -= start_multiplier * fx / self.start.mass
        self.start.vy -= start_multiplier * fy / self.start.mass
        self.end.vx += end_multiplier * fx / self.end.mass
        self.end.vy += end_multiplier * fy / self.end.mass


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
 