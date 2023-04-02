"""
We pulled out the graph IO methods to keep the graph file entirely about updating and drawing
"""
import csv
import os.path
from graph import SpringMassGraph
from vertex import Vertex
from edge import Edge


def load_from_csv(graph: SpringMassGraph, filename: str) -> None:
    """Load a graph from a csv file with the following format:

    - The first line of the file consists of two integers (n, k), where n is the number of vertices
        and k is the number of edges
    - The next n lines consist of data needed to instantiate a vertex (x, y, pinned)
        where x is the x-coordinate, y is the y-coordinate, and pinned is a bool representing 
        whether a vertex is pinned or not
    - The next k lines consist of data needed to instantiate an edge
        which consists of three numbers (i,j,d) where i is the list index of the
        edge's start node, j is the list index of the edge's end node, and d is the
        initial distance between nodes 

    Do nothing if the file is empty or doesn't exist.

    Preconditions:
    - The file is properly formatted
    """
    if not os.path.isfile(filename):
        return

    with open(filename, "r") as csvfile:
        lines = list(csv.reader(csvfile))

    if len(lines) == 0:
        return

    graph.reset()
    n, k = int(lines[0][0]), int(lines[0][1])

    # Add the vertices
    for i in range(1, n + 1):
        x, y, pinned = float(lines[i][0]), float(lines[i][1]), lines[i][2]
        vertex = Vertex(x, y)
        if pinned == 'True':
            vertex.pinned = True
        graph.vertices.append(vertex)

    # Add the edges
    for i in range(n + 1, n + k + 1):
        i, j, d = int(lines[i][0]), int(lines[i][1]), float(lines[i][2])
        edge = Edge(graph.vertices[i], graph.vertices[j])
        edge.initial_distance = d
        graph.edges.append(edge)


def save_to_csv(graph: SpringMassGraph, filename: str) -> None:
    """Save a graph to an csv file with the following format:

    - The first line of the file consists of two integers (n, k), where n is the number of vertices
        and k is the number of edges
    - The next n lines consist of data needed to instantiate a vertex (x, y, pinned)
        where x is the x-coordinate, y is the y-coordinate, and pinned is a bool representing 
        whether a vertex is pinned or not
    - The next k lines consist of data needed to instantiate an edge
        which consists of three numbers (i,j,d) where i is the list index of the
        edge's start node, j is the list index of the edge's end node, and d is the
        initial distance between nodes 
    
    Do nothing if the file write fails.
    """
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        n, k = len(graph.vertices), len(graph.edges)

        writer.writerow([n, k])
        for vertex in graph.vertices:
            writer.writerow([vertex.x, vertex.y, vertex.pinned])

        for edge in graph.edges:
            i = graph.vertices.index(edge.start)
            j = graph.vertices.index(edge.end)
            writer.writerow([i, j, edge.initial_distance])


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(
        config={
            "extra-imports": ["csv", "os.path", "graph", "edge", "vertex"],
            "allowed-io": ["load_from_csv", "save_to_csv"],
            "max-line-length": 100
        }
    )
