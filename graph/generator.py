import random

from graph.graph import Graph


def generate_random_graph(num_vertices, edge_probability, seed):
    # Се користи локален генератор за истото seed секогаш да даде ист граф,
    # без да се менува глобалната random состојба на програмата.
    rng = random.Random(seed)

    graph = Graph(num_vertices)

    # Секој можен недиректиран раб се разгледува точно еднаш.
    # Работ се додава независно со веројатност edge_probability.
    for u in range(num_vertices):
        for v in range(u + 1, num_vertices):
            if rng.random() < edge_probability:
                graph.add_edge(u, v)

    return graph