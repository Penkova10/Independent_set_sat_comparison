from graph.graph import Graph
from algorithms.backtracking import independent_set_backtracking


def test_backtracking_positive_case():
    graph = Graph(4)

    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)

    found, solution = independent_set_backtracking(graph, 2)

    assert found is True
    assert len(solution) >= 2


def test_backtracking_negative_case():
    graph = Graph(4)

    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)

    found, solution = independent_set_backtracking(graph, 3)

    assert found is False
    assert solution == []