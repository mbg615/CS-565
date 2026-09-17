"""
run_search.py

Convenience script for running your search implementations.

Examples
--------
Run all algorithms:
    python run_search.py --map maps/map1.txt --algorithm all

Run one algorithm:
    python run_search.py --map maps/map2.txt --algorithm ucs

Show the returned path on the grid:
    python run_search.py --map maps/map3.txt --algorithm astar --show-path
"""

from __future__ import annotations

import argparse
from math import isinf

from grid import GridProblem
from search import astar, bfs, ucs


ALGORITHMS = {
    "bfs": bfs,
    "ucs": ucs,
    "astar": astar,
}


def print_result(name: str, problem: GridProblem, result, show_path: bool) -> None:
    print(f"\n{name.upper()}")
    print("-" * len(name))

    if not result.found:
        print("No path found.")
        print(f"Nodes expanded: {result.nodes_expanded}")
        return

    valid, message = problem.validate_path(result.path)
    recomputed_cost = problem.path_cost(result.path)

    print(f"Path found:      {result.found}")
    print(f"Path valid:      {valid} ({message})")
    print(f"Steps:           {result.steps}")
    print(f"Reported cost:   {result.cost:g}")
    print(f"Recomputed cost: {recomputed_cost:g}")
    print(f"Nodes expanded:  {result.nodes_expanded}")

    if result.cost != recomputed_cost:
        print("WARNING: reported cost does not match the path's actual cost.")

    if show_path:
        print("\nPath:")
        print(problem.render(result.path))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--map",
        required=True,
        help="Path to a map file, e.g. maps/map1.txt",
    )
    parser.add_argument(
        "--algorithm",
        choices=["bfs", "ucs", "astar", "all"],
        default="all",
        help="Search algorithm to run.",
    )
    parser.add_argument(
        "--show-path",
        action="store_true",
        help="Print the grid with the returned path marked by *.",
    )
    args = parser.parse_args()

    problem = GridProblem.from_file(args.map)

    print("GRID")
    print("----")
    print(problem.render())
    print(f"\nStart: {problem.start}")
    print(f"Goal:  {problem.goal}")

    names = list(ALGORITHMS) if args.algorithm == "all" else [args.algorithm]

    for name in names:
        try:
            result = ALGORITHMS[name](problem)
        except NotImplementedError as exc:
            print(f"\n{name.upper()}")
            print("-" * len(name))
            print(exc)
            continue

        print_result(name, problem, result, args.show_path)


if __name__ == "__main__":
    main()
