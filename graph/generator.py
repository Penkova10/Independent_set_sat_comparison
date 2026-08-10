import random

from graph.graph import Graph


def generate_random_graph(num_vertices, edge_probability, seed):
    random.seed(seed)

    graph = Graph(num_vertices)

    for u in range(num_vertices):
        for v in range(u + 1, num_vertices):
            if random.random() < edge_probability:
                graph.add_edge(u, v)

    return graph