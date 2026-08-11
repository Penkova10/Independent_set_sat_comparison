from time import perf_counter
from statistics import median
import csv
import os

from algorithms.backtracking import independent_set_backtracking
from algorithms.validator import is_valid_solution
from sat.encoder import create_sat_encoding
from sat.minisat_solver import solve_with_minisat
from sat.cadical_solver import solve_with_cadical
from graph.generator import generate_random_graph
from experiments.experiment_config import (
    VERTEX_COUNTS,
    EDGE_PROBABILITIES,
    SEEDS,
    K_RATIOS,
    REPETITIONS,
    BACKTRACKING_TIMEOUT
)


def benchmark_instance(
    graph,
    k,
    repetitions=REPETITIONS,
    backtracking_timeout_seconds=BACKTRACKING_TIMEOUT
):
    results = {}

    # --------------------------------------------------
    # Backtracking
    # --------------------------------------------------

    backtracking_times = []
    backtracking_found = None
    backtracking_solution = None
    backtracking_timed_out = False

    for _ in range(repetitions):
        try:
            start = perf_counter()

            backtracking_found, backtracking_solution = (
                independent_set_backtracking(
                    graph,
                    k,
                    timeout_seconds=backtracking_timeout_seconds
                )
            )

            elapsed_time = perf_counter() - start
            backtracking_times.append(elapsed_time)

        except TimeoutError:
            backtracking_timed_out = True
            backtracking_found = None
            backtracking_solution = []
            break

    if backtracking_timed_out:
        # Кај timeout го запишуваме лимитот како цензурирано време,
        # а не го претставуваме како успешно измерено време на решавање.
        backtracking_time = float(backtracking_timeout_seconds)
        backtracking_valid = None
    else:
        backtracking_time = median(backtracking_times)

        # Валидацијата се прави надвор од мереното време на алгоритмот.
        backtracking_valid = (
            is_valid_solution(graph, backtracking_solution, k)
            if backtracking_found
            else True
        )

    results["backtracking"] = {
        "found": backtracking_found,
        "solution": backtracking_solution,
        "time": backtracking_time,
        "timeout": backtracking_timed_out,
        "valid": backtracking_valid
    }

    # --------------------------------------------------
    # SAT encoding
    # --------------------------------------------------

    encoding_times = []

    clauses = None
    num_variables = None
    num_clauses = None

    for _ in range(repetitions):
        start = perf_counter()

        clauses, num_variables, num_clauses = create_sat_encoding(
            graph,
            k
        )

        elapsed_time = perf_counter() - start
        encoding_times.append(elapsed_time)

    encoding_time = median(encoding_times)

    # --------------------------------------------------
    # MiniSat
    # --------------------------------------------------

    minisat_times = []
    minisat_found = None
    minisat_solution = None

    for _ in range(repetitions):
        start = perf_counter()

        minisat_found, minisat_solution = solve_with_minisat(
            clauses,
            graph.num_vertices
        )

        elapsed_time = perf_counter() - start
        minisat_times.append(elapsed_time)

    minisat_time = median(minisat_times)

    results["minisat"] = {
        "found": minisat_found,
        "solution": minisat_solution,
        "num_variables": num_variables,
        "num_clauses": num_clauses,
        "encoding_time": encoding_time,
        "solver_time": minisat_time,
        "total_time": encoding_time + minisat_time,
        "valid": (
            is_valid_solution(graph, minisat_solution, k)
            if minisat_found
            else True
        )
    }

    # --------------------------------------------------
    # CaDiCaL
    # --------------------------------------------------

    cadical_times = []
    cadical_found = None
    cadical_solution = None

    for _ in range(repetitions):
        start = perf_counter()

        cadical_found, cadical_solution = solve_with_cadical(
            clauses,
            graph.num_vertices
        )

        elapsed_time = perf_counter() - start
        cadical_times.append(elapsed_time)

    cadical_time = median(cadical_times)

    results["cadical"] = {
        "found": cadical_found,
        "solution": cadical_solution,
        "num_variables": num_variables,
        "num_clauses": num_clauses,
        "encoding_time": encoding_time,
        "solver_time": cadical_time,
        "total_time": encoding_time + cadical_time,
        "valid": (
            is_valid_solution(graph, cadical_solution, k)
            if cadical_found
            else True
        )
    }

    return results


def run_experiments():
    all_results = []

    for n in VERTEX_COUNTS:
        for p in EDGE_PROBABILITIES:
            for seed in SEEDS:
                for k_ratio in K_RATIOS:

                    # Моменталните конфигурации даваат целобројни вредности за k.
                    # int() намерно го задржува постојното заокружување надолу.
                    k = max(1, int(n * k_ratio))

                    graph = generate_random_graph(
                        num_vertices=n,
                        edge_probability=p,
                        seed=seed
                    )

                    results = benchmark_instance(
                        graph,
                        k,
                        repetitions=REPETITIONS,
                        backtracking_timeout_seconds=BACKTRACKING_TIMEOUT
                    )

                    all_results.append({
                        "n": n,
                        "p": p,
                        "seed": seed,
                        "k": k,
                        "results": results
                    })

                    print(
                        f"Finished: n={n}, p={p}, "
                        f"seed={seed}, k={k}"
                    )

    return all_results


def save_results_to_csv(
    all_results,
    filename="results/benchmark_results.csv"
):
    # Ако е зададена сопствена папка во filename, ја креираме таа папка.
    output_directory = os.path.dirname(filename)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "n",
            "p",
            "seed",
            "k",
            "method",
            "found",
            "solution",
            "valid",
            "timeout",
            "num_variables",
            "num_clauses",
            "encoding_time",
            "solver_time",
            "total_time"
        ])

        for instance in all_results:
            n = instance["n"]
            p = instance["p"]
            seed = instance["seed"]
            k = instance["k"]

            for method, result in instance["results"].items():

                if method == "backtracking":
                    timeout = result["timeout"]
                    num_variables = ""
                    num_clauses = ""
                    encoding_time = ""
                    solver_time = result["time"]
                    total_time = result["time"]

                else:
                    timeout = False
                    num_variables = result["num_variables"]
                    num_clauses = result["num_clauses"]
                    encoding_time = result["encoding_time"]
                    solver_time = result["solver_time"]
                    total_time = result["total_time"]

                writer.writerow([
                    n,
                    p,
                    seed,
                    k,
                    method,
                    result["found"],
                    result["solution"],
                    result["valid"],
                    timeout,
                    num_variables,
                    num_clauses,
                    encoding_time,
                    solver_time,
                    total_time
                ])


def run_pilot_experiments():
    from experiments.pilot_config import (
        PILOT_VERTEX_COUNTS,
        PILOT_EDGE_PROBABILITIES,
        PILOT_SEEDS,
        PILOT_K_RATIOS,
        PILOT_REPETITIONS,
        PILOT_BACKTRACKING_TIMEOUT
    )

    all_results = []

    for n in PILOT_VERTEX_COUNTS:
        for p in PILOT_EDGE_PROBABILITIES:
            for seed in PILOT_SEEDS:
                for k_ratio in PILOT_K_RATIOS:

                    # Истиот начин на пресметка на k се користи во сите режими.
                    k = max(1, int(n * k_ratio))

                    graph = generate_random_graph(
                        num_vertices=n,
                        edge_probability=p,
                        seed=seed
                    )

                    results = benchmark_instance(
                        graph,
                        k,
                        repetitions=PILOT_REPETITIONS,
                        backtracking_timeout_seconds=PILOT_BACKTRACKING_TIMEOUT
                    )

                    all_results.append({
                        "n": n,
                        "p": p,
                        "seed": seed,
                        "k": k,
                        "results": results
                    })

                    print(
                        f"Pilot finished: n={n}, p={p}, "
                        f"seed={seed}, k={k}"
                    )

    return all_results


def run_final_experiments():
    from experiments.final_config import (
        FINAL_VERTEX_COUNTS,
        FINAL_EDGE_PROBABILITIES,
        FINAL_SEEDS,
        FINAL_K_RATIOS,
        FINAL_REPETITIONS,
        BACKTRACKING_TIMEOUT as FINAL_BACKTRACKING_TIMEOUT
    )

    all_results = []

    for n in FINAL_VERTEX_COUNTS:
        for p in FINAL_EDGE_PROBABILITIES:
            for seed in FINAL_SEEDS:
                for k_ratio in FINAL_K_RATIOS:

                    # Истиот начин на пресметка на k се користи во сите режими.
                    k = max(1, int(n * k_ratio))

                    graph = generate_random_graph(
                        num_vertices=n,
                        edge_probability=p,
                        seed=seed
                    )

                    results = benchmark_instance(
                        graph,
                        k,
                        repetitions=FINAL_REPETITIONS,
                        backtracking_timeout_seconds=FINAL_BACKTRACKING_TIMEOUT
                    )

                    all_results.append({
                        "n": n,
                        "p": p,
                        "seed": seed,
                        "k": k,
                        "results": results
                    })

                    print(
                        f"Final finished: n={n}, p={p}, "
                        f"seed={seed}, k={k}"
                    )

    return all_results
