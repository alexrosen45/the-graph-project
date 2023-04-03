"""CSC111 Final Project: Measurements & Results Generator

Module Description
==================
This module contains the code for solving an optimization problem of finding the minimum
pootential energy of a pyramid graph.

Copyright Information
=====================
This file is licensed under the MIT License
"""
from graph_types import PyramidGraph, SpringMassGraph


def calculate_potential_score(graph: SpringMassGraph) -> float:
    """Calculates the total potential energy when running a graph for 10 seconds or until
    it stops moving and the potential energy is no longer changing
    """
    potential_score = 0.0
    for _i in range(10 * 60 * 16):
        old_potential_energy = graph.metrics.elastic_potential_energy
        graph.step()
        if round(old_potential_energy, 5) == round(graph.metrics.elastic_potential_energy, 5) and \
                round(graph.metrics.kinetic_energy, 5) == 0.0:
            break
        potential_score += graph.metrics.elastic_potential_energy / (60.0 * 16.0)

    return round(potential_score, 4)


def run_with_config(graph: SpringMassGraph, config: list[float]) -> float:
    """Run simulation with given constants"""
    spring_constant, friction, gravity = config
    graph.spring_constant = spring_constant
    graph.friction = friction
    graph.gravity = gravity
    return calculate_potential_score(graph)


def main() -> None:
    """The main measurements function"""
    config = [0.03, 0.98, 0.01]
    clamps = ((0.01, 0.1), (0.9, 0.99), (0.01, 0.2))
    graph = PyramidGraph(6, 50)
    for _j in range(40):
        for i in range(3):
            # Use gradient descent to optimize the three parameters
            left = max(clamps[i][0], config[i] - (clamps[i][1] - clamps[i][0]) / 20)
            right = min(clamps[i][1], config[i] + (clamps[i][1] - clamps[i][0]) / 20)
            config[i] = left
            left_run = run_with_config(graph, config)
            config[i] = right
            right_run = run_with_config(graph, config)
            if left_run < right_run:
                config[i] = left
    print(config)


if __name__ == "__main__":
    main()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(
        config={
            "extra-imports": ["graph_types"],
            "max-line-length": 120,
            "allowed-io": ["main"]
        }
    )
