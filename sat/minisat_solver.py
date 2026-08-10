from pysat.solvers import Minisat22


def solve_with_minisat(clauses, num_vertices):
    with Minisat22(bootstrap_with=clauses) as solver:
        is_sat = solver.solve()

        if not is_sat:
            return False, []

        model = solver.get_model()

        selected_vertices = []

        for vertex in range(num_vertices):
            variable = vertex + 1

            if variable in model:
                selected_vertices.append(vertex)

        return True, selected_vertices