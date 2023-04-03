"""CSC 111 Final Project: Generate Datasets

Module Description
==================
Generate graphs and save them to csv files, creating our datasets

Copyright Information
=====================
This file is licensed under the MIT License
"""
from graph_types import CompleteGraph, WheelGraph, PyramidGraph, ClothGraph
from graph_io import save_to_csv


def main() -> None:
    """Our main function which generates and writes graphs"""

    # wheels
    graph = WheelGraph(3, 100)
    save_to_csv(graph, "data/w3.csv")
    graph = WheelGraph(4, 100)
    save_to_csv(graph, "data/w4.csv")
    graph = WheelGraph(5, 100)
    save_to_csv(graph, "data/w5.csv")
    graph = WheelGraph(6, 100)
    save_to_csv(graph, "data/w6.csv")
    graph = WheelGraph(8, 100)
    save_to_csv(graph, "data/w8.csv")
    graph = WheelGraph(10, 100)
    save_to_csv(graph, "data/w10.csv")
    graph = WheelGraph(20, 100)
    save_to_csv(graph, "data/w20.csv")

    # complete graphs
    graph = CompleteGraph(3, 100)
    save_to_csv(graph, "data/k3.csv")
    graph = CompleteGraph(4, 100)
    save_to_csv(graph, "data/k4.csv")
    graph = CompleteGraph(7, 100)
    save_to_csv(graph, "data/k7.csv")
    graph = CompleteGraph(10, 100)
    save_to_csv(graph, "data/k10.csv")

    # Triangle graphs
    graph = PyramidGraph(2, 50)
    save_to_csv(graph, "data/tri2.csv")
    graph = PyramidGraph(4, 50)
    save_to_csv(graph, "data/tri2.csv")
    graph = PyramidGraph(6, 99)
    save_to_csv(graph, "data/tri6.csv")

    # cloth graphs
    graph = ClothGraph(50, 50, 10)
    save_to_csv(graph, "data/cloth1.csv")
    graph = ClothGraph(50, 25, 10)
    save_to_csv(graph, "data/cloth2.csv")


if __name__ == "__main__":
    main()

    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(
        config={
            "extra-imports": ["tkinter", "tkinter.filedialog", "graph_types", "graph_io"],
            "allowed-io": [],
            "max-line-length": 100,
        }
    )
