from pysat.card import CardEnc


def create_sat_encoding(graph, k):
    clauses = []

    # 1. Соседни јазли не смеат да бидат избрани заедно
    for u in range(graph.num_vertices):
        for v in graph.adjacency[u]:
            if u < v:
                clauses.append([-(u + 1), -(v + 1)])

    # 2. Мора да бидат избрани најмалку k јазли
    variables = list(range(1, graph.num_vertices + 1))

    cardinality = CardEnc.atleast(
        lits=variables,
        bound=k,
        top_id=graph.num_vertices
    )

    clauses.extend(cardinality.clauses)

    num_variables = cardinality.nv
    num_clauses = len(clauses)

    return clauses, num_variables, num_clauses