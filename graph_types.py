"""
This is how we generate our various datasets, by constructing various graphs through inheritance
"""
import math
from graph import SpringMassGraph, WIDTH, HEIGHT
from edge import Edge
from vertex import Vertex


class WheelGraph(SpringMassGraph):
    """
    Create a wheel graph with n edges
    """
    def __init__(self, n: int, length: int) -> None:
        super().__init__()

        center_x, center_y = (WIDTH / 2, HEIGHT / 2)
        center = Vertex(center_x, center_y)
        self.vertices.append(center)

        old_vertex = None
        first_vertex = None
        for i in range(0, n):
            theta = (math.pi * 2) * (i / n)
            new_vertex = Vertex(
                center_x + length * math.cos(theta),
                center_y + length * math.sin(theta)
            )
            if i == 0:
                first_vertex = new_vertex
            self.vertices.append(new_vertex)
            self.edges.append(Edge(center, new_vertex))
            if old_vertex is not None:
                self.edges.append(Edge(old_vertex, new_vertex))
            old_vertex = new_vertex

        self.edges.append(Edge(old_vertex, first_vertex))


class CompleteGraph(SpringMassGraph):
    """
    Create a fully connected graph with vertices in a circle
    """
    def __init__(self, n: int, length: int) -> None:
        super().__init__()

        center_x, center_y = (WIDTH / 2, HEIGHT / 2)
        for i in range(0, n):
            theta = (math.pi * 2) * (i / n)
            new_vertex = Vertex(
                center_x + length * math.cos(theta),
                center_y + length * math.sin(theta)
            )
            self.vertices.append(new_vertex)

        for i in range(0, n):
            for j in range(i + 1, n):
                self.edges.append(Edge(self.vertices[i], self.vertices[j]))


class ClothGraph(SpringMassGraph):
    """
    Create a cloth like graph.
    """
    def __init__(self, x_len: int, y_len: int, vertex_dist: int) -> None:
        super().__init__(gravity=0.01, friction=0.99, spring_constant=0.5)

        start_x = WIDTH / 2 - ((x_len * vertex_dist) / 2)

        grid = []
        for i in range(0, y_len):
            row = []
            for j in range(0, x_len):
                vertex = Vertex(start_x + j * vertex_dist, i * vertex_dist)
                row.append(vertex)
                self.vertices.append(vertex)
            grid.append(row)

        # pin certain nodes
        grid[0][0].pinned = True
        grid[0][x_len - 1].pinned = True
        grid[0][int(x_len / 3)].pinned = True
        grid[0][int(2 * x_len / 3)].pinned = True

        for i in range(0, y_len):
            for j in range(0, x_len):
                if i > 0:
                    self.edges.append(Edge(grid[i][j], grid[i - 1][j]))
                if j > 0:
                    self.edges.append(Edge(grid[i][j], grid[i][j - 1]))


class PyramidGraph(SpringMassGraph):
    """
    A work in progress graph to make tall structures efficiently
    """
    def __init__(self, count: int, vertex_dist: float) -> None:
        super().__init__()

        # Generate an equilateral triangle subdivided into equilateral triangles
        start_x = WIDTH / 2 - ((count * vertex_dist) / 2)

        grid = []
        for i in range(count):
            row = []
            for j in range(i + 1):
                vertex = Vertex(start_x + j * vertex_dist, i * vertex_dist)
                row.append(vertex)
                self.vertices.append(vertex)
            grid.append(row)

        for i in range(count):
            for j in range(i + 1):
                if i > 0:
                    self.edges.append(Edge(grid[i][j], grid[i - 1][j]))
                if j > 0:
                    self.edges.append(Edge(grid[i][j], grid[i][j - 1]))


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(
        config={
            "extra-imports": ["math", "graph", "edge", "vertex"],
            "allowed-io": [],
            "max-line-length": 100,
        }
    )
