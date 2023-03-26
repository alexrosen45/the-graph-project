from graph.vertex import Vertex


class Edge:
    """Massless spring, applies spring forces"""
    initial_distance = 5
    start: Vertex
    end: Vertex

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.initial_distance = (
            (start.x - end.x) ** 2 + (start.y - end.y) ** 2) ** 0.5
