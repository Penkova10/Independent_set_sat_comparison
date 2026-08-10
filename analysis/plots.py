import os
import matplotlib.pyplot as plt

from analysis.statistics import (
    load_results,
    median_time_by_n,
    median_time_by_density,
    count_wins
)


def plot_time_by_n(filename="results/final_results.csv"):
    rows = load_results(filename)
    data = median_time_by_n(rows)

    methods = ["backtracking", "minisat", "cadical"]
    n_values = sorted(data.keys())

    os.makedirs("results/plots", exist_ok=True)

    for method in methods:
        times = [
            data[n][method]
            for n in n_values
        ]

        plt.plot(
            n_values,
            times,
            marker="o",
            label=method
        )

    plt.xlabel("Number of vertices (n)")
    plt.ylabel("Median total time (seconds)")
    plt.title("Runtime by Graph Size")
    plt.yscale("log")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("results/plots/runtime_by_n.png")
    plt.close()


def plot_time_by_density(filename="results/final_results.csv"):
    rows = load_results(filename)
    data = median_time_by_density(rows)

    methods = ["backtracking", "minisat", "cadical"]
    densities = sorted(data.keys())

    os.makedirs("results/plots", exist_ok=True)

    for method in methods:
        times = [
            data[p][method]
            for p in densities
        ]

        plt.plot(
            densities,
            times,
            marker="o",
            label=method
        )

    plt.xlabel("Edge probability (p)")
    plt.ylabel("Median total time (seconds)")
    plt.title("Runtime by Graph Density")
    plt.yscale("log")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("results/plots/runtime_by_density.png")
    plt.close()


def plot_method_wins(filename="results/final_results.csv"):
    rows = load_results(filename)
    wins = count_wins(rows)

    methods = ["backtracking", "minisat", "cadical"]

    values = [
        wins.get(method, 0)
        for method in methods
    ]

    os.makedirs("results/plots", exist_ok=True)

    plt.bar(methods, values)

    plt.xlabel("Method")
    plt.ylabel("Number of fastest instances")
    plt.title("Fastest Method per Instance")

    plt.tight_layout()
    plt.savefig("results/plots/method_wins.png")
    plt.close()

def plot_encoding_size(filename="results/final_results.csv"):
    rows = load_results(filename)

    # MiniSat и CaDiCaL користат ист SAT encoding,
    # затоа земаме само MiniSat редови за да нема дупликати.
    sat_rows = [
        row for row in rows
        if row["method"] == "minisat"
    ]

    n_values = sorted(set(row["n"] for row in sat_rows))

    median_variables = []
    median_clauses = []

    from statistics import median

    for n in n_values:
        rows_for_n = [
            row for row in sat_rows
            if row["n"] == n
        ]

        variables = [
            int(row["num_variables"])
            for row in rows_for_n
        ]

        clauses = [
            int(row["num_clauses"])
            for row in rows_for_n
        ]

        median_variables.append(median(variables))
        median_clauses.append(median(clauses))

    os.makedirs("results/plots", exist_ok=True)

    plt.plot(
        n_values,
        median_variables,
        marker="o",
        label="CNF variables"
    )

    plt.plot(
        n_values,
        median_clauses,
        marker="o",
        label="CNF clauses"
    )

    plt.xlabel("Number of vertices (n)")
    plt.ylabel("Median encoding size")
    plt.title("SAT Encoding Size by Graph Size")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("results/plots/encoding_size.png")
    plt.close()

def generate_all_plots(filename="results/final_results.csv"):
    plot_time_by_n(filename)
    plot_time_by_density(filename)
    plot_method_wins(filename)
    plot_encoding_size(filename)

    print("Plots saved to results/plots/")