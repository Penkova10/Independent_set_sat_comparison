from time import perf_counter

from algorithms.validator import is_independent_set


def independent_set_backtracking(graph, k, timeout_seconds=None):
    vertices = list(range(graph.num_vertices))

    start_time = perf_counter()

    def backtrack(index, selected):

        # Проверка за timeout
        if (
            timeout_seconds is not None
            and perf_counter() - start_time >= timeout_seconds
        ):
            raise TimeoutError("Backtracking time limit exceeded.")

        # Најден е Independent Set со најмалку k јазли
        if len(selected) >= k:
            return True, selected.copy()

        # Стигнавме до крајот без решение
        if index == len(vertices):
            return False, []

        # Pruning:
        # дури и ако ги земеме сите преостанати јазли,
        # нема да можеме да стигнеме до k
        remaining = len(vertices) - index

        if len(selected) + remaining < k:
            return False, []

        vertex = vertices[index]

        # Пробај да го избереш тековниот јазол
        candidate = selected + [vertex]

        if is_independent_set(graph, candidate):
            found, solution = backtrack(
                index + 1,
                candidate
            )

            if found:
                return True, solution

        # Пробај без тековниот јазол
        return backtrack(
            index + 1,
            selected
        )

    return backtrack(0, [])