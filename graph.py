"""CSC 111 Final Project: Spring Mass Graph

Module Description
==================
This is the critical file for our project.
It handles the main graph creation, updating and drawing

Copyright Information
=====================
This file is licensed under the MIT License
"""
import pygame
from edge import Edge
from vertex import Vertex


class SpringMassGraph:
    """Spring mass graph."""

    vertices: list
    edges: list

    width: int = 800
    height: int = 600

    spring_constant: float
    friction: float
    gravity: float

    elastic_potential_energy: float = 0.0
    kinetic_energy: float = 0.0

    SUBSTEPS: int = 16
    EDGE_CREATION_RADIUS: float = 100
    DRAG_RADIUS: float = 10

    # colors for drawing graph
    BLUE: tuple = (0, 0, 255)
    BLACK: tuple = (0, 0, 0)
    WHITE: tuple = (255, 255, 255)
    LIGHT_GREEN: tuple = (128, 255, 212)

    def __init__(
        self,
        spring_constant: float = 0.03,
        friction: float = 0.98,
        gravity: float = 0.01
    ) -> None:
        self.vertices = []
        self.edges = []

        self.spring_constant = spring_constant
        self.friction = friction
        self.gravity = gravity
    

    def update_width_and_height(self, width: int, height: int) -> None:
        """Updates graph width and height"""
        self.width = width
        self.height = height

    def draw(self, screen: pygame.Surface) -> None:
        """Draw graph on pygame screen."""
        screen.fill(self.WHITE)
        mouse = pygame.mouse.get_pos()

        is_near_vertex = any(
            ((vertex.x - mouse[0]) ** 2 + (vertex.y - mouse[1]) ** 2)
            < self.DRAG_RADIUS ** 2
            for vertex in self.vertices
        )
        if is_near_vertex:
            pygame.draw.circle(screen, self.LIGHT_GREEN,
                               mouse, self.DRAG_RADIUS)
        else:
            pygame.draw.circle(screen, self.LIGHT_GREEN, mouse,
                               self.EDGE_CREATION_RADIUS)

        self._draw_edges(screen)
        self._draw_vertices(screen)

    def add_new_vertex(self, x: float, y: float) -> None:
        """Add to vertex to graph as position (x, y)."""
        new_vertex = Vertex(x, y, randomize=True)

        # add edges within edge creation radius
        for v in self.vertices:
            distance = (v.x - new_vertex.x) ** 2 + (v.y - new_vertex.y) ** 2
            if distance < self.EDGE_CREATION_RADIUS ** 2:
                new_edge = Edge(v, new_vertex)
                self.edges.append(new_edge)

        self.vertices.append(new_vertex)

    def remove_last_vertex(self) -> None:
        """Remove the last vertex added to the graph."""
        if len(self.vertices) > 0:
            v = self.vertices.pop()
            self.edges = [e for e in self.edges if v not in {e.start, e.end}]

    def reset(self) -> None:
        """Remove all vertices and edges from self."""
        self.vertices = []
        self.edges = []

    def run_substeps(self) -> None:
        """Run self.step self.SUBSTEPS times."""
        for _i in range(self.SUBSTEPS):
            self.step()

    def _draw_vertices(self, screen: pygame.Surface) -> None:
        """Draw self.vertices on pygame screen."""
        for v in self.vertices:
            pygame.draw.circle(screen, self.BLACK, (v.x, v.y), v.mass)

    def _draw_edges(self, screen: pygame.Surface) -> None:
        """Draw self.edges on pygame screen."""
        for edge in self.edges:
            dx = edge.start.x - edge.end.x
            dy = edge.start.y - edge.end.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            delta_len = min(abs(distance - edge.initial_distance), 10)
            gray_color = delta_len * 255 // 10
            color = (gray_color, (255 - gray_color), 0)
            pygame.draw.line(
                screen, color,
                (edge.start.x, edge.start.y),
                (edge.end.x, edge.end.y)
            )

    def step(self) -> None:
        """Execute a physics logic step for the simulation, updating all vertices and edges."""
        self.elastic_potential_energy = 0.0
        self._update_edges()
        self._update_vertices()
        self._clamp_vertices()

    def _update_vertices(self) -> None:
        """Update vertices for simulation step relative to change in time."""
        self.kinetic_energy = 0.0
        for v in self.vertices:
            velocity = v.update(self.friction, self.gravity, self.height, self.width)
            self.kinetic_energy += 0.5 * (velocity ** 2) * v.mass

    def _update_edges(self) -> None:
        """Update edges for simulation step relative to change in time."""
        for edge in self.edges:
            dx = edge.start.x - edge.end.x
            dy = edge.start.y - edge.end.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            dlen = max(
                min(
                    self.spring_constant * (distance - edge.initial_distance),
                    9),
                -9
            )
            if distance == 0:
                distance += 0.0001
            fx = dx * dlen / distance
            fy = dy * dlen / distance

            potential_energy = self.spring_constant * ((distance - edge.initial_distance) ** 2)
            self.elastic_potential_energy += potential_energy

            edge.update(fx, fy)

    def _clamp_vertices(self) -> None:
        """Clamp vertex coordinates."""
        for v in self.vertices:
            v.clamp(self.height, self.width)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(
        config={
            "extra-imports": [
                "csv",
                "edge",
                "os.path",
                "pygame",
                "vertex",
            ],
            "max-line-length": 100,
        }
    )
