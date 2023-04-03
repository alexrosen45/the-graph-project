"""CSC111 Final Project: Metrics Rendering Functions

Module Description
===================
This module contains the code for rendering the metrics of the simulation.

Copyright Information
=====================
This file is licensed under the MIT License.
"""
import pygame
from graph import SpringMassGraph


class Metrics:
    """
    Metrics class

    Instance Attributes:
    font: Comic Sans, used for rendering
    """
    font: pygame.font.Font

    POTENTIAL_ENERGY_LOCATION: tuple[int, int] = (5, 5)
    KINETIC_ENERGY_LOCATION: tuple[int, int] = (5, 35)

    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize metrics class"""
        self.font = pygame.font.SysFont('Comic Sans MS', 15)
        self._render(0.0, 0.0, screen)

    def update_widgets(self, graph: SpringMassGraph, screen: pygame.Surface) -> None:
        """Update widgets to reflect results of computation"""
        self._render(graph.metrics.elastic_potential_energy, graph.metrics.kinetic_energy, screen)

    def _render(self, potential_energy: float, kinetic_energy: float, screen: pygame.Surface) -> None:
        """Render widgets"""
        potential_energy_text = self.font.render(
            'Elastic Potential Energy: ' + str(round(potential_energy, 2)), False, (0, 0, 0)
        )
        screen.blit(potential_energy_text, self.POTENTIAL_ENERGY_LOCATION)

        kinetic_energy_text = self.font.render(
            'Kinetic Energy: ' + str(round(kinetic_energy, 2)), False, (0, 0, 0)
        )
        screen.blit(kinetic_energy_text, self.KINETIC_ENERGY_LOCATION)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(
        config={
            "extra-imports": [
                "pygame",
                "graph"
            ],
            "max-line-length": 120,
        }
    )
