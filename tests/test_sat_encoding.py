from graph.graph import Graph
from algorithms.validator import is_valid_solution
from sat.encoder import create_sat_encoding
from sat.minisat_solver import solve_with_minisat


def test_sat_encoding_positive_case():
    graph = Graph(4)

    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)

    clauses, num_variables, num_clauses = create_sat_encoding(
        graph,
        2
    )

    # За секој раб мора да постои клаузула
    # која забранува двете темиња да бидат избрани заедно.
    assert [-1, -2] in clauses
    assert [-1, -3] in clauses
    assert [-2, -4] in clauses
    assert [-3, -4] in clauses

    # Бројот на SAT променливи ги вклучува оригиналните
    # променливи за темињата и евентуалните помошни променливи.
    assert num_variables >= graph.num_vertices
    assert num_clauses == len(clauses)

    found, solution = solve_with_minisat(
        clauses,
        graph.num_vertices
    )

    assert found is True
    assert len(solution) >= 2

    # SAT моделот мора да даде навистина валидно independent set решение.
    assert is_valid_solution(graph, solution, 2) is True


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