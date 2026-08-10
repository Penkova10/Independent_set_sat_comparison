from graph.graph import Graph
from algorithms.backtracking import independent_set_backtracking
from sat.encoder import create_sat_encoding
from sat.minisat_solver import solve_with_minisat
from sat.cadical_solver import solve_with_cadical


def solve_with_all_methods(graph, k):
    # Backtracking
    backtracking_found, _ = independent_set_backtracking(graph, k)

    # SAT encoding
    clauses, _, _ = create_sat_encoding(graph, k)

    # MiniSat
    minisat_found, _ = solve_with_minisat(
        clauses,
        graph.num_vertices
    )

    # CaDiCaL
    cadical_found, _ = solve_with_cadical(
        clauses,
        graph.num_vertices
    )

    return (
        backtracking_found,
        minisat_found,
        cadical_found
    )


def test_methods_agree_positive_case():
    graph = Graph(4)

    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)

    results = solve_with_all_methods(graph, 2)

    assert results == (True, True, True)


def test_methods_agree_negative_case():
    graph = Graph(4)

    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)

    results = solve_with_all_methods(graph, 3)

    assert results == (False, False, False)


def test_complete_graph():
    graph = Graph(5)

    for u in range(5):
        for v in range(u + 1, 5):
            graph.add_edge(u, v)

    # Во complete graph максималниот independent set има големина 1.
    results = solve_with_all_methods(graph, 2)

    assert results == (False, False, False)


def test_empty_graph():
    graph = Graph(5)

    # Нема ребра, па сите 5 темиња можат да бидат избрани.
    results = solve_with_all_methods(graph, 5)

    assert results == (True, True, True)