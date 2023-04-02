"""
This is the critical file for our project.
It handles the main graph creation, updating and drawing
"""
import pygame
from edge import Edge
from vertex import Vertex

(WIDTH, HEIGHT) = (800, 600)

# colours for drawing graph
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREEN = (128, 255, 212)


class SpringMassGraph:
    """Spring mass graph."""

    vertices: list
    edges: list

    spring_constant: float
    friction: float
    ground_friction: float
    gravity: float

    SUBSTEPS: int = 10
    EDGE_CREATION_RADIUS: float = 100
    DRAG_RADIUS: float = 10

    def __init__(
        self,
        spring_constant: float = 0.02,
        friction: float = 0.02,
        ground_friction: float = 0.02,
        gravity: float = 0.02
    ) -> None:
        self.vertices = []
        self.edges = []

        self.spring_constant = spring_constant
        self.ground_friction = ground_friction
        self.friction = friction
        self.gravity = gravity

    def draw(self, screen: pygame.Surface) -> None:
        """Draw graph on pygame screen."""
        screen.fill(WHITE)
        mouse = pygame.mouse.get_pos()

        is_near_vertex = any(
            (vertex.x - mouse[0]) ** 2 + (vertex.y - mouse[1]) ** 2 < self.DRAG_RADIUS ** 2
            for vertex in self.vertices
        )
        if is_near_vertex:
            pygame.draw.circle(screen, LIGHT_GREEN, mouse, self.DRAG_RADIUS)
        else:
            pygame.draw.circle(screen, LIGHT_GREEN, mouse,
                               self.EDGE_CREATION_RADIUS)

        self._draw_edges(screen)
        self._draw_vertices(screen)

    def add_new_vertex(self, x: float, y: float) -> None:
        """Add to vertex to graph as position (x, y)."""
        new_vertex = Vertex(x, y)

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

    def get_time_change(self, time_elapsed: float) -> float:
        """Return time change based on time elapsed."""
        return time_elapsed / 1000 * 60

    def run_substeps(self) -> None:
        """Run self.step self.SUBSTEPS times."""
        for _i in range(self.SUBSTEPS):
            self._step(16)

    def _draw_vertices(self, screen: pygame.Surface) -> None:
        """Draw self.vertices on pygame screen."""
        for v in self.vertices:
            pygame.draw.circle(screen, BLACK, (v.x, v.y), v.mass)

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

    def _step(self, time_elapsed: int) -> None:
        """Execute a physics logic step for the simulation, updating all vertices and edges."""
        # calculate change in time
        dt = self.get_time_change(time_elapsed)

        self._update_vertices(dt)
        self._update_edges(dt)
        self._clamp_vertices()

    def _update_vertices(self, dt: float) -> None:
        """Update vertices for simulation step relative to change in time."""
        for v in self.vertices:
            v.update(self.friction, self.gravity, dt)

    def _update_edges(self, dt: float) -> None:
        """Update edges for simulation step relative to change in time."""
        for edge in self.edges:
            dx = edge.start.x - edge.end.x
            dy = edge.start.y - edge.end.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            dlen = max(min(self.spring_constant * (distance - edge.initial_distance), 9), -9)
            fx = dx * dlen / distance * dt
            fy = dy * dlen / distance * dt
            edge.update(fx, fy)

    def _clamp_vertices(self) -> None:
        """Clamp vertex coordinates."""
        for v in self.vertices:
            v.clamp(HEIGHT, WIDTH)


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
