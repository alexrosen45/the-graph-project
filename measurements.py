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
    potential_score = 0.0
    for _ in range(10 * 60 * 16):
        old_potential_energy = graph.elastic_potential_energy
        graph.step()
        if round(old_potential_energy, 5) != round(graph.elastic_potential_energy, 5) \
            or round(graph.kinetic_energy, 5) != 0.0:
            potential_score += graph.elastic_potential_energy / (60.0 * 16.0)
        else:
            break
    return round(potential_score, 4)

def run_with_config(graph: SpringMassGraph, config: list[float]) -> float:
    """Run simulation with given constants"""
    graph.spring_constant = config[0]
    graph.friction = config[1]
    graph.gravity = config[2]
    return calculate_potential_score(graph)

if __name__ == "__main__":
    config = [0.03, 0.98, 0.01]
    clamps = ((0.01, 0.1), (0.9, 0.99), (0.01, 0.2))
    graph = PyramidGraph(6, 50)
    for _j in range(40):
        for i in range(3):
            left = max(clamps[i][0], config[i] - (clamps[i][1] - clamps[i][0]) / 20)
            right = min(clamps[i][1], config[i] + (clamps[i][1] - clamps[i][0]) / 20)
            config[i] = left
            left_run = run_with_config(graph, config)
            config[i] = right
            right_run = run_with_config(graph, config)
            if left_run < right_run:
                config[i] = left
    print(config)

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
    