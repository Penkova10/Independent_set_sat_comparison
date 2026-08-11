from pysat.solvers import Minisat22


def solve_with_minisat(clauses, num_vertices):
    with Minisat22(bootstrap_with=clauses) as solver:
        is_sat = solver.solve()

        if not is_sat:
            return False, []

        model = solver.get_model()

        # Set овозможува поефикасна проверка кои SAT променливи
        # што ги претставуваат оригиналните јазли имаат вредност True.
        model_set = set(model)

        selected_vertices = []

        for vertex in range(num_vertices):
            variable = vertex + 1

            if variable in model_set:
                selected_vertices.append(vertex)

        return True, selected_vertices