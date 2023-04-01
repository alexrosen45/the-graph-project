"""
Main simulation file
"""
import pygame
from graph import SpringMassGraph
from sliders import load_sliders, load_slider_textboxes, update_sliders, draw_slider_text
import file_dialog


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

    # load sliders and slider textboxes
    gravity_slider, gravity_output, friction_slider, friction_output, spring_slider, spring_output = load_sliders(
        screen
    )

    gravity_text, friction_text, spring_text = load_slider_textboxes()

    while running:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.KEYDOWN:
                # save the graph configuration
                if event.key == pygame.K_s:
                    file_name = file_dialog.ask_file().name
                    graph.save_to_csv(file_name)
                # load a graph configuration
                if event.key == pygame.K_l:
                    file_name = file_dialog.prompt_file()
                    graph.load_from_csv(file_name)

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

        # update slider, draw slider text, and update graph attributes
        update_sliders(graph, gravity_slider, friction_slider, spring_slider,
                       gravity_output, friction_output, spring_output, ev)
        draw_slider_text(screen, gravity_text, friction_text, spring_text)

        pygame.display.update()


if __name__ == "__main__":
    main()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(
        config={
            "extra-imports": ["pygame", "pygame_widgets", "file_dialog", "graph.graph", "sliders.sliders"],
            "allowed-io": [],
            "max-line-length": 100,
        }
    )
