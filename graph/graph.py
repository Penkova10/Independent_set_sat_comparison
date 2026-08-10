class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices

        self.adjacency = {
            vertex: set()
            for vertex in range(num_vertices)
        }

    def add_edge(self, u, v):
        self.adjacency[u].add(v)
        self.adjacency[v].add(u)

    def are_adjacent(self, u, v):
        return v in self.adjacency[u]