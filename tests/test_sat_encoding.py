from graph.graph import Graph
from sat.encoder import create_sat_encoding
from sat.minisat_solver import solve_with_minisat


def test_sat_encoding_positive_case():
    graph = Graph(4)

    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)

    clauses, _, _ = create_sat_encoding(graph, 2)

    found, solution = solve_with_minisat(
        clauses,
        graph.num_vertices
    )

    assert found is True
    assert len(solution) >= 2


def test_sat_encoding_negative_case():
    graph = Graph(4)

    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)

    clauses, _, _ = create_sat_encoding(graph, 3)

    found, solution = solve_with_minisat(
        clauses,
        graph.num_vertices
    )

    assert found is False
    assert solution == []