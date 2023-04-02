"""
Main simulation file
"""
import pygame
from graph import SpringMassGraph
from graph_io import load_from_csv, save_to_csv
from graph_types import ClothGraph
from sliders import load_sliders, load_slider_textboxes, update_sliders, draw_slider_text
from file_dialog import FileDialog


WIDTH, HEIGHT = 800, 600


class GraphEventHandler:
    """A helper class to manage dragging of vertices"""
    dragging: list | None
    lastmouse: tuple
    file_dialog: FileDialog

    def __init__(self) -> None:
        self.file_dialog = FileDialog()
        self.dragging = None
        self.lastmouse = (0, 0)

    def check_drag_on_mousedown(self, graph: SpringMassGraph, pos: tuple) -> None:
        """Check if vertex is being dragged on mouse down."""
        posx, posy = pos
        for v in graph.vertices:
            if (v.x - posx) ** 2 + (v.y - posy) ** 2 < graph.DRAG_RADIUS ** 2:
                if self.dragging is None:
                    self.dragging = []
                self.dragging.append(v)
                v.pinned = True

    def handle_graph_mouse(self, graph: SpringMassGraph, event: pygame.event.Event) -> tuple:
        """Handle dragging of graphs."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            self.check_drag_on_mousedown(graph, pos)
            self.lastmouse = pos

        if event.type == pygame.MOUSEMOTION:
            if self.dragging is not None:
                newmouse = pygame.mouse.get_pos()
                for v in self.dragging:
                    v.x += newmouse[0] - self.lastmouse[0]
                    v.y += newmouse[1] - self.lastmouse[1]
                self.lastmouse = newmouse

        # add new vertex
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if self.dragging is None:
                graph.add_new_vertex(pos[0], pos[1])
            else:
                for v in self.dragging:
                    v.pinned = False
                self.dragging = None

    def handle_event(
        self,
        graph: SpringMassGraph,
        event: pygame.event.Event
    ) -> None:
        """Handle pygame events for main."""
        if event.type == pygame.KEYDOWN:
            # save the graph configuration
            if event.key == pygame.K_s:
                file_name = self.file_dialog.ask_file()
                if file_name is not None:
                    save_to_csv(graph, file_name.name)
            # load a graph configuration
            if event.key == pygame.K_l:
                file_name = self.file_dialog.prompt_file()
                load_from_csv(graph, file_name)

        if event.type == pygame.KEYDOWN:
            # remove last vertex added
            if event.key == pygame.key.key_code("z"):
                graph.remove_last_vertex()

            # reset graph
            if event.key == pygame.key.key_code("r"):
                graph.reset()

        self.handle_graph_mouse(graph, event)


def main() -> None:
    """
    Initialize pygame, create the screen, initialize
    our graph, and execute the simulation's main loop.
    """
    # This event handler needs to be above pygame.init, see file_dialog.py for more details
    event_handler = GraphEventHandler()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    graph = ClothGraph(50, 25, 10)

    running = True

    # load sliders and slider textboxes
    sliders = load_sliders(screen, graph)
    gravity_slider, gravity_output = sliders[0], sliders[1]
    friction_slider, friction_output = sliders[2], sliders[3]
    spring_slider, spring_output = sliders[4], sliders[5]

    textboxes = load_slider_textboxes()

    while running:
        ev = pygame.event.get()

        # handle events
        for event in ev:
            event_handler.handle_event(graph, event)

            # handle quitting
            if event.type == pygame.QUIT:
                running = False

        graph.run_substeps()
        graph.draw(screen)
        clock.tick(60)

        # update slider, draw slider text, and update graph attributes
        update_sliders(graph, (gravity_slider, friction_slider, spring_slider),
                       (gravity_output, friction_output, spring_output), ev)
        draw_slider_text(screen, textboxes[0], textboxes[1], textboxes[2])

        pygame.display.update()


if __name__ == "__main__":
    main()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(
        config={
            "extra-imports": [
                "pygame", "pygame_widgets", "file_dialog",
                "graph", "graph_io", "graph_types", "sliders"
            ],
            "allowed-io": [],
            "max-line-length": 100,
            # get rid of incorrect "pygame has no" error
            "disable": ['E1101'],
        }
    )
