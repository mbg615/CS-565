"""
run_search.py

Convenience script for running your Programming Lab 2 implementations.

Examples
--------
Run both algorithms from the empty board:
    python run_search.py --position empty --algorithm all

Run both algorithms from a provided mid-game position:
    python run_search.py --position a --algorithm all

Run only Alpha-Beta:
    python run_search.py --position c --algorithm alphabeta
"""

from __future__ import annotations

import argparse

from search import alphabeta, minimax
from tic_tac_toe import TicTacToe, state_from_string


POSITIONS = {
    # Empty board.
    "empty": ".........",

    # X to move; X has an immediate winning move.
    "a": "XX.OO....",

    # X to move; another immediate-win position with a different best action.
    "b": "XO.XO....",

    # O to move; O has an immediate winning move.
    "c": "XOX.OX...",
}


ALGORITHMS = {
    "minimax": minimax,
    "alphabeta": alphabeta,
}


def print_result(name: str, result) -> None:
    print(f"\n{name.upper()}")
    print("-" * len(name))

    print(f"Minimax value:        {result.value}")
    print(f"Selected action:      {result.action}")
    print(f"Nodes visited:        {result.nodes_visited}")
    print(f"Terminal evaluations: {result.terminal_evaluations}")
    print(f"Cutoffs:              {result.cutoffs}")

    if result.action is not None:
        row, col = divmod(result.action, 3)
        print(f"Selected square:      row {row}, column {col}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--position",
        choices=list(POSITIONS),
        default="empty",
        help="Provided test position to search.",
    )
    parser.add_argument(
        "--algorithm",
        choices=["minimax", "alphabeta", "all"],
        default="all",
        help="Game-search algorithm to run.",
    )
    args = parser.parse_args()

    game = TicTacToe()
    state = state_from_string(POSITIONS[args.position])

    print("POSITION")
    print("--------")
    print(game.render(state))

    if game.terminal(state):
        print("\nTerminal state.")
    else:
        print(f"\nPlayer to move: {game.player(state)}")

    names = list(ALGORITHMS) if args.algorithm == "all" else [args.algorithm]

    results = {}

    for name in names:
        try:
            result = ALGORITHMS[name](game, state)
        except NotImplementedError as exc:
            print(f"\n{name.upper()}")
            print("-" * len(name))
            print(exc)
            continue

        results[name] = result
        print_result(name, result)

    if "minimax" in results and "alphabeta" in results:
        same_value = results["minimax"].value == results["alphabeta"].value
        same_action = results["minimax"].action == results["alphabeta"].action

        print("\nCOMPARISON")
        print("----------")
        print(f"Same value:  {same_value}")
        print(f"Same action: {same_action}")

        if results["minimax"].nodes_visited > 0:
            reduction = (
                1
                - results["alphabeta"].nodes_visited
                / results["minimax"].nodes_visited
            ) * 100
            print(f"Node reduction: {reduction:.2f}%")


if __name__ == "__main__":
    main()
