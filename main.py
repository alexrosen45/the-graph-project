"""
Main simulation file
"""

import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from graph.graph import SpringMassGraph


(width, height) = (800, 600)


def main():
    """
    Initialize pygame, create the screen, initialize
    our graph, and execute the simulation's main loop.
    """
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    dragging = None
    graph = SpringMassGraph()

    running = True
    lastmouse = pygame.mouse.get_pos()

    # slider
    slider = Slider(
        screen, 100, 100, 800, 40, min=0, max=99, step=1
    )
    output = TextBox(
        screen, 475, 200, 50, 50, fontSize=30
    )
    # output.disable()  # Act as label instead of textbox

    while running:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.KEYDOWN:
                # save the graph configuration
                if event.key == pygame.K_s:
                    graph.save_to_csv('graph.csv')
                # load a graph configuration
                if event.key == pygame.K_l:
                    graph.load_from_csv('graph.csv')

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx, posy = pygame.mouse.get_pos()
                for v in graph.vertices:
                    if (v.x - posx) ** 2 + (v.y - posy) ** 2 < graph.DRAG_RADIUS ** 2:
                        if dragging is None:
                            dragging = []
                        dragging.append(v)
                        v.pinned = True
                lastmouse = (posx, posy)

            if event.type == pygame.MOUSEMOTION:
                if dragging is not None:
                    newmouse = pygame.mouse.get_pos()
                    for v in dragging:
                        v.x += newmouse[0] - lastmouse[0]
                        v.y += newmouse[1] - lastmouse[1]
                    lastmouse = newmouse

            # add new vertex
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if dragging is None:
                    graph.add_new_vertex(pos[0], pos[1])
                else:
                    for v in dragging:
                        v.pinned = False
                    dragging = None

            if event.type == pygame.KEYDOWN:
                # remove last vertex added
                if event.key == pygame.key.key_code("z"):
                    graph.remove_last_vertex()

                # reset graph
                if event.key == pygame.key.key_code("r"):
                    graph.reset()

            if event.type == pygame.QUIT:
                running = False

        graph.run_substeps()
        graph.draw(screen)

        clock.tick(60)

        # update slider
        output.setText(slider.getValue())
        pygame_widgets.update(ev)

        print(slider.getValue())
        print(slider.colour)

        pygame.display.update()


if __name__ == "__main__":
    main()
