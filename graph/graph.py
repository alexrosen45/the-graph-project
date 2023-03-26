from graph.edge import Edge
from graph.vertex import Vertex
import pygame

(width, height) = (800, 600)


# colours for drawing graph
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREEN = (128, 255, 212)


class SpringMassGraph:
    """Spring mass graph."""
    vertices: list
    edges: list

    SPRING_CONSTANT: float
    FRICTION: float
    GROUND_FRICTION: float
    GRAVITY: float

    SUBSTEPS = 10
    EDGE_CREATION_RADIUS = 100
    DRAG_RADIUS = 10

    def __init__(self, spring_constant=0.02, friction=0.02, ground_friction=0.02, gravity=0.01) -> None:
        """Initialize blank graph"""
        self.vertices = []
        self.edges = []

        self.SPRING_CONSTANT = spring_constant
        self.GROUND_FRICTION = ground_friction
        self.FRICTION = friction
        self.GRAVITY = gravity

    def draw(self, screen) -> None:
        """Draw graph on pygame screen."""
        # setup
        screen.fill(WHITE)
        mouse = pygame.mouse.get_pos()

        is_near_vertex = False
        for vertex in self.vertices:
            if (vertex.x - mouse[0]) ** 2 + (vertex.y - mouse[1]) ** 2 < self.DRAG_RADIUS ** 2:
                is_near_vertex = True
                break
        if is_near_vertex:
            pygame.draw.circle(screen, LIGHT_GREEN,
                               mouse, self.DRAG_RADIUS)
        else:
            pygame.draw.circle(screen, LIGHT_GREEN,
                               mouse, self.EDGE_CREATION_RADIUS)

        for edge in self.edges:
            dx = edge.start.x - edge.end.x
            dy = edge.start.y - edge.end.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            dlen = (min(abs(distance - edge.initial_distance), 10))
            tension = dlen * 255 // 10
            color = (tension, (255 - tension), 0)
            pygame.draw.line(screen, color,
                             (edge.start.x, edge.start.y),
                             (edge.end.x, edge.end.y))

        for vertex in self.vertices:
            pygame.draw.circle(
                screen, BLACK, (vertex.x, vertex.y), vertex.mass)

        pygame.display.update()

    def _step(self, time_elapsed: int) -> None:
        """Execute a physics logic step for the simulation, updating all vertices and edges."""
        # calculate change in time
        dt = self.get_time_change(time_elapsed)

        self._update_vertices(dt)
        self._update_edges(dt)
        self._clamp_vertices()

    def get_time_change(self, time_elapsed) -> float:
        """Return time change based on time elapsed."""
        return time_elapsed / 1000 * 60

    def _update_vertices(self, dt: float) -> None:
        """Update vertices for simulation step relative to change in time."""
        for vertex in self.vertices:
            vertex.vx *= (1 - (self.FRICTION * dt))
            vertex.vy *= (1 - (self.FRICTION * dt))
            vertex.vy += self.GRAVITY * dt
            if not vertex.pinned:
                vertex.x += (vertex.vx * dt)
                vertex.y += (vertex.vy * dt)

    def _update_edges(self, dt: float) -> None:
        """Update edges for simulation step relative to change in time."""
        for edge in self.edges:
            dx = edge.start.x - edge.end.x
            dy = edge.start.y - edge.end.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            dlen = (max(min(distance - edge.initial_distance, 10), -10))
            fx = self.SPRING_CONSTANT * dx * dlen / distance * dt
            fy = self.SPRING_CONSTANT * dy * dlen / distance * dt
            edge.start.vx -= fx / edge.start.mass
            edge.start.vy -= fy / edge.start.mass
            edge.end.vx += fx / edge.end.mass
            edge.end.vy += fy / edge.end.mass

    def _clamp_vertices(self) -> None:
        """Clamp vertex coordinates."""
        for vertex in self.vertices:
            if not vertex.pinned:
                vertex.y = min(vertex.y, height)
                vertex.x = max(min(vertex.x, width), 0)
