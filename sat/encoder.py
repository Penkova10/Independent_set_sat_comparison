from pysat.card import CardEnc, EncType


def create_sat_encoding(graph, k):
    clauses = []

    # 1. Соседни јазли не смеат да бидат избрани заедно.
    # Сортирањето обезбедува детерминистички редослед на CNF клаузулите.
    for u in range(graph.num_vertices):
        for v in sorted(graph.adjacency[u]):
            if u < v:
                clauses.append([-(u + 1), -(v + 1)])

    # 2. Мора да бидат избрани најмалку k јазли.
    # Променливите 1..n одговараат на јазлите 0..n-1.
    variables = list(range(1, graph.num_vertices + 1))

    # Експлицитно користиме sequential-counter encoding
    # за методологијата да не зависи од default вредност на PySAT.
    cardinality = CardEnc.atleast(
        lits=variables,
        bound=k,
        top_id=graph.num_vertices,
        encoding=EncType.seqcounter
    )

    clauses.extend(cardinality.clauses)

    # cardinality.nv ги вклучува и помошните SAT променливи.
    num_variables = cardinality.nv
    num_clauses = len(clauses)

    return clauses, num_variables, num_clauses