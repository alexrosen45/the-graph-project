from graph.edge import Edge
from graph.vertex import Vertex
import pygame
import csv
import os.path

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

    def __init__(self, spring_constant=0.02, friction=0.02, ground_friction=0.02, gravity=0.02) -> None:
        self.vertices = []
        self.edges = []

        self.SPRING_CONSTANT = spring_constant
        self.GROUND_FRICTION = ground_friction
        self.FRICTION = friction
        self.GRAVITY = gravity

    def draw(self, screen) -> None:
        """Draw graph on pygame screen."""
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

        self._draw_edges(screen)
        self._draw_vertices(screen)

    def add_new_vertex(self, x, y) -> None:
        """Add to vertex to graph as position (x, y)."""
        new_vertex = Vertex(x, y)

        # add edges within edge creation radius
        for v in self.vertices:
            if (v.x - new_vertex.x) ** 2 + (v.y - new_vertex.y) ** 2 < self.EDGE_CREATION_RADIUS ** 2:
                new_edge = Edge(v, new_vertex)
                self.edges.append(new_edge)

        self.vertices.append(new_vertex)

    def remove_last_vertex(self) -> None:
        """Remove the last vertex added to the graph."""
        if len(self.vertices) > 0:
            v = self.vertices.pop()
            self.edges = [
                e for e in self.edges if e.start != v and e.end != v
            ]

    def reset(self) -> None:
        """Remove all vertices and edges from self."""
        self.vertices = []
        self.edges = []

    def get_time_change(self, time_elapsed: float) -> float:
        """Return time change based on time elapsed."""
        return time_elapsed / 1000 * 60

    def run_substeps(self) -> None:
        """Run self.step self.SUBSTEPS times."""
        for _ in range(self.SUBSTEPS):
            self._step(16)

    def _draw_vertices(self, screen) -> None:
        """Draw self.vertices on pygame screen."""
        for v in self.vertices:
            pygame.draw.circle(screen, BLACK, (v.x, v.y), v.mass)

    def _draw_edges(self, screen) -> None:
        """Draw self.edges on pygame screen."""
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
            v.update(self.FRICTION, self.GRAVITY, dt)

    def _update_edges(self, dt: float) -> None:
        """Update edges for simulation step relative to change in time."""
        for edge in self.edges:
            dx = edge.start.x - edge.end.x
            dy = edge.start.y - edge.end.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            dlen = (max(min(distance - edge.initial_distance, 10), -10))
            fx = self.SPRING_CONSTANT * dx * dlen / distance * dt
            fy = self.SPRING_CONSTANT * dy * dlen / distance * dt
            edge.update(fx, fy)

    def _clamp_vertices(self) -> None:
        """Clamp vertex coordinates."""
        for v in self.vertices:
            v.clamp(height, width)

    def load_from_csv(self, filename: str) -> None:
        """Load a graph from a csv file with the following format:

        - The first line of the consists of two integers n,k. The number of vertices n
        and the number of edges k
        - The next n lines will consist of data needed to instantiate a vertex
        (x, y)
        - The next k lines will consist of data needed to instantiate an edge
        which would consist of two numbers i,j, where i is the list index of the 
        edge's start node and j is the list index of the edge's end node
        (i, j)

        Do nothing if the file is empty or doesn't exist

        Preconditions:
        - The file is properly formatted
        """
        if not os.path.isfile(filename):
            return

        with open(filename, 'r') as csvfile:
            lines = list(csv.reader(csvfile))

        if len(lines) == 0:
            return

        n, k = int(lines[0][0]), int(lines[0][1])

        # Add the vertices
        self.vertices = []
        for i in range(1, n + 1):
            x, y = float(lines[i][0]), float(lines[i][1])
            vertex = Vertex(x, y)
            self.vertices.append(vertex)

        # Add the edges
        self.edges = []
        for i in range(n + 1, n + k + 1):
            i, j = int(lines[i][0]), int(lines[i][1])
            edge = Edge(self.vertices[i], self.vertices[j])
            self.edges.append(edge)

    def save_to_csv(self, filename: str) -> None:
        """Save a graph to an csv file with the following format:

        - The first line of the consists of two integers n,k. The number of vertices n
        and the number of edges k
        - The next n lines will consist of data needed to instantiate a vertex
        (x, y)
        - The next k lines will consist of data needed to instantiate an edge
        which would consist of two numbers i,j, where i is the list index of the 
        edge's start node and j is the list index of the edge's end node
        (i, j)
        """
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            n, k = len(self.vertices), len(self.edges)

            writer.writerow([n, k])
            for vertex in self.vertices:
                writer.writerow([vertex.x, vertex.y])

            for edge in self.edges:
                i = self.vertices.index(edge.start)
                j = self.vertices.index(edge.end)
                writer.writerow([i, j])
