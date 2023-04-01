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

    # sliders
    gravity_slider = Slider(
        screen, 600, 50, 100, 10, min=0, max=0.2, step=0.005
    )
    gravity_slider.setValue(0.02)
    gravity_output = TextBox(
        screen, 720, 45, 40, 25, fontSize=20
    )

    friction_slider = Slider(
        screen, 600, 80, 100, 10, min=0, max=0.2, step=0.005
    )
    friction_slider.setValue(0.02)
    friction_output = TextBox(
        screen, 720, 75, 40, 25, fontSize=20
    )

    spring_slider = Slider(
        screen, 600, 110, 100, 10, min=0, max=0.2, step=0.005
    )
    spring_slider.setValue(0.02)
    spring_output = TextBox(
        screen, 720, 105, 40, 25, fontSize=20
    )

    # slider textboxes
    comic_sans = pygame.font.SysFont('Comic Sans MS', 15)
    gravity_text = comic_sans.render('Gravity', False, (0, 0, 0))
    friction_text = comic_sans.render('Friction', False, (0, 0, 0))
    spring_text = comic_sans.render('Spring Tension', False, (0, 0, 0))

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

        # update slider and graph attributes
        gravity = gravity_slider.getValue()
        friction = friction_slider.getValue()
        spring = spring_slider.getValue()

        graph.gravity = gravity
        graph.friction = friction
        graph.spring_constant = spring

        gravity_output.setText(gravity_slider.getValue())
        pygame_widgets.update(ev)
        friction_output.setText(friction_slider.getValue())
        pygame_widgets.update(ev)
        spring_output.setText(spring_slider.getValue())
        pygame_widgets.update(ev)

        # update slider text
        screen.blit(gravity_text, (540, 45))
        screen.blit(friction_text, (535, 75))
        screen.blit(spring_text, (490, 105))

        pygame.display.update()


if __name__ == "__main__":
    main()
