def is_independent_set(graph, vertices):
    # Independant set не може да ги содржи истите јазли повеќе од еднаш
    if len(vertices) != len(set(vertices)):
        return False

    if any(v < 0 or v >= graph.num_vertices for v in vertices):
        return False

    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            if graph.are_adjacent(vertices[i], vertices[j]):
                return False

    return True


def is_valid_solution(graph, vertices, k):
    if len(vertices) < k:
        return False

    return is_independent_set(graph, vertices)