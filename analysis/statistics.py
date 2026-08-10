import csv
from collections import defaultdict
from statistics import median


def load_results(filename="results/final_results.csv"):
    rows = []

    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["n"] = int(row["n"])
            row["p"] = float(row["p"])
            row["k"] = int(row["k"])
            row["seed"] = int(row["seed"])
            row["total_time"] = float(row["total_time"])
            row["timeout"] = row["timeout"] == "True"
            row["valid"] = row["valid"] == "True"

            rows.append(row)

    return rows


def median_time_by_n(rows):
    grouped = defaultdict(lambda: defaultdict(list))

    for row in rows:
        grouped[row["n"]][row["method"]].append(row["total_time"])

    result = {}

    for n, methods in grouped.items():
        result[n] = {}

        for method, times in methods.items():
            result[n][method] = median(times)

    return result


def median_time_by_density(rows):
    grouped = defaultdict(lambda: defaultdict(list))

    for row in rows:
        grouped[row["p"]][row["method"]].append(row["total_time"])

    result = {}

    for p, methods in grouped.items():
        result[p] = {}

        for method, times in methods.items():
            result[p][method] = median(times)

    return result


def count_timeouts(rows):
    return sum(
        1
        for row in rows
        if row["method"] == "backtracking"
        and row["timeout"]
    )


def count_wins(rows):
    instances = defaultdict(list)

    for row in rows:
        key = (
            row["n"],
            row["p"],
            row["seed"],
            row["k"]
        )

        instances[key].append(row)

    wins = defaultdict(int)

    for instance_rows in instances.values():
        fastest = min(
            instance_rows,
            key=lambda row: row["total_time"]
        )

        wins[fastest["method"]] += 1

    return dict(wins)


def all_results_valid(rows):
    return all(row["valid"] for row in rows)


def print_summary(filename="results/final_results.csv"):
    rows = load_results(filename)

    print("=== FINAL EXPERIMENT SUMMARY ===")
    print()

    print("Total rows:", len(rows))
    print("All results valid:", all_results_valid(rows))
    print("Backtracking timeouts:", count_timeouts(rows))

    print("\nMedian total time by n:")

    by_n = median_time_by_n(rows)

    for n in sorted(by_n):
        print(f"n = {n}")

        for method, time_value in by_n[n].items():
            print(f"  {method}: {time_value:.6f} s")

    print("\nMedian total time by density:")

    by_density = median_time_by_density(rows)

    for p in sorted(by_density):
        print(f"p = {p}")

        for method, time_value in by_density[p].items():
            print(f"  {method}: {time_value:.6f} s")

    print("\nFastest method wins:")

    wins = count_wins(rows)

    for method, count in wins.items():
        print(f"  {method}: {count}")