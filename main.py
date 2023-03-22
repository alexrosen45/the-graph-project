"""
Main simulation file
"""

import pygame
import math

(width, height) = (800, 600)
BLUE = (0, 0, 255)
EDGE_CREATION_RADIUS = 100

SPRING_CONSTANT = 0.1
FRICTION = 0.98
GROUND_FRICTION = 0.98
GRAVITY = 0.1


class Vertex:
    """
    Vertex class that stores a mass in a system of springs
    """
    mass: float
    x: float
    y: float
    vx: float
    vy: float

    def __init__(self, x, y):
        self.mass = 5
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0


class Edge:
    """Massless spring, applies spring forces"""
    initial_distance = 5
    start: Vertex
    end: Vertex

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.initial_distance = ((start.x - end.x) ** 2 + (start.y - end.y) ** 2) ** 0.5


vertices = []
edges = []


def step():
    """Execute a physics logic step for the simulation, updating all vertices and edges"""
    for vertex in vertices:
        vertex.vx *= FRICTION
        vertex.vy *= FRICTION
        if vertex.y + 2 * vertex.mass < height:
            vertex.vy += GRAVITY
        vertex.x += vertex.vx
        vertex.y += vertex.vy
        if vertex.y - vertex.mass >= height:
            vertex.y = height - vertex.mass
            if math.fabs(vertex.vy) > 1:
                vertex.vy = -math.fabs(vertex.vy) * 0.2
            else:
                vertex.vy = 0
            vertex.vx *= GROUND_FRICTION

    for edge in edges:
        dx = edge.start.x - edge.end.x
        dy = edge.start.y - edge.end.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        fx = SPRING_CONSTANT * dx * (1 - edge.initial_distance / distance)
        fy = SPRING_CONSTANT * dy * (1 - edge.initial_distance / distance)
        edge.start.vx -= fx / edge.start.mass
        edge.start.vy -= fy / edge.start.mass
        edge.end.vx += fx / edge.end.mass
        edge.end.vy += fy / edge.end.mass


def draw(screen):
    """
    Draw all vertices and edges to the screen
    """

    screen.fill((0, 0, 0))

    mouse = pygame.mouse.get_pos()
    pygame.draw.circle(screen, (50, 50, 50), mouse, EDGE_CREATION_RADIUS)

    for vertex in vertices:
        pygame.draw.circle(screen, BLUE, (vertex.x, vertex.y), vertex.mass)

    for edge in edges:
        pygame.draw.line(screen, BLUE, (edge.start.x, edge.start.y), (edge.end.x, edge.end.y))

    pygame.display.update()


def main():
    """
    Initialize pygame, create the screen, and execute the simulation's main loop
    """
    pygame.init()
    screen = pygame.display.set_mode((width, height))

    running = True
    while running:
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                new_v = Vertex(pos[0], pos[1])
                for v in vertices:
                    if (v.x - new_v.x) ** 2 + (v.y - new_v.y) ** 2 < EDGE_CREATION_RADIUS ** 2:
                        new_edge = Edge(v, new_v)
                        edges.append(new_edge)
                vertices.append(new_v)

            if event.type == pygame.QUIT:
                running = False

        step()
        draw(screen)


if __name__ == "__main__":
    main()
