"""Metrics Rendering Functions"""

import pygame
from graph import SpringMassGraph

class Metrics:
    font: pygame.font.Font
    elastic_potential_energy_location: tuple[int, int] = (5, 5)
    kinetic_energy_location: tuple[int, int] = (5, 35)

    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize metrics class"""
        self.font = pygame.font.SysFont('Comic Sans MS', 15)
        self._render(0.0, 0.0, screen)

    def update_widgets(self, graph: SpringMassGraph, screen: pygame.Surface) -> None:
        """Update widgets to reflect results of computation"""
        self._render(graph.elastic_potential_energy, graph.kinetic_energy, screen)

    def _render(self, elastic_potential_energy: float, kinetic_energy: float, screen: pygame.Surface) -> None:
        """Render widgets"""
        elastic_potential_energy_text = self.font.render('Elastic Potential Energy: ' + str(round(elastic_potential_energy, 2)), False, (0, 0, 0))
        screen.blit(elastic_potential_energy_text, self.elastic_potential_energy_location)

        kinetic_energy_text = self.font.render('Kinetic Energy: ' + str(round(kinetic_energy, 2)), False, (0, 0, 0))
        screen.blit(kinetic_energy_text, self.kinetic_energy_location)
    

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
            "max-line-length": 120,
        }
    )
