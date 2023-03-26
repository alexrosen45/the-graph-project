"""
Main simulation file
"""

import pygame
import math

from graph.vertex import Vertex
from graph.edge import Edge


(width, height) = (800, 600)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREEN = (128, 255, 212)
EDGE_CREATION_RADIUS = 100

SPRING_CONSTANT = 0.5
FRICTION = 0.02
GROUND_FRICTION = 0.02
GRAVITY = 0.01

vertices = []
edges = []


def step(time_elapsed: int):
    """Execute a physics logic step for the simulation, updating all vertices and edges"""
    dt = time_elapsed / 1000 * 60
    for vertex in vertices:
        vertex.vx *= (1 - (FRICTION * dt))
        vertex.vy *= (1 - (FRICTION * dt))
        # if vertex.y + 2 * vertex.mass < height:
        vertex.vy += GRAVITY * dt
        vertex.x += (vertex.vx * dt)
        vertex.y += (vertex.vy * dt)

    for edge in edges:
        dx = edge.start.x - edge.end.x
        dy = edge.start.y - edge.end.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        dlen = (max(min(distance - edge.initial_distance, 10), -10))
        fx = SPRING_CONSTANT * dx * dlen / distance * dt
        fy = SPRING_CONSTANT * dy * dlen / distance * dt
        edge.start.vx -= fx / edge.start.mass
        edge.start.vy -= fy / edge.start.mass
        edge.end.vx += fx / edge.end.mass
        edge.end.vy += fy / edge.end.mass

    for vertex in vertices:
        vertex.y = min(vertex.y, height)
        # if math.fabs(vertex.vy) > 1:
        #     vertex.vy = -math.fabs(vertex.vy) * 0.2
        # else:
        # vertex.vy = 0
        # vertex.vx *= (1 - (GROUND_FRICTION * dt))


def draw(screen):
    """
    Draw all vertices and edges to the screen
    """
    # change background color
    screen.fill(WHITE)

    mouse = pygame.mouse.get_pos()
    pygame.draw.circle(screen, LIGHT_GREEN, mouse, EDGE_CREATION_RADIUS)

    for edge in edges:
        pygame.draw.line(screen, BLACK, (edge.start.x,
                         edge.start.y), (edge.end.x, edge.end.y))

    for vertex in vertices:
        pygame.draw.circle(screen, BLACK, (vertex.x, vertex.y), vertex.mass)

    pygame.display.update()


def main():
    """
    Initialize pygame, create the screen, and execute the simulation's main loop
    """
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

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

        step(clock.get_time())
        draw(screen)
        clock.tick(60)


if __name__ == "__main__":
    main()
