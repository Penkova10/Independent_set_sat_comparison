from experiments.benchmark import (
    run_final_experiments,
    save_results_to_csv
)
from analysis.statistics import print_summary
from analysis.plots import generate_all_plots


def main():
    print("Running final experiments...")

    final_results = run_final_experiments()

    save_results_to_csv(
        final_results,
        filename="results/final_results.csv"
    )

    print("\nFinal experiments completed.")
    print("Number of instances:", len(final_results))
    print("Results saved to results/final_results.csv")

    print()
    print_summary("results/final_results.csv")

    print()
    generate_all_plots("results/final_results.csv")


if __name__ == "__main__":
    main()