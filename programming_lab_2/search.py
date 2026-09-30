"""
search.py
Programming Lab 2 — Adversarial Search with Minimax and Alpha-Beta Pruning

THIS IS THE MAIN FILE YOU WILL EDIT.

Implement:
    1. minimax
    2. alphabeta

You may add private helper functions.

Do not change the required function names or parameter lists.
"""

from __future__ import annotations

from dataclasses import dataclass

from tic_tac_toe import Action, State, TicTacToe


@dataclass
class SearchResult:
    """
    Standard result returned by both game-search algorithms.

    Attributes
    ----------
    value:
        Minimax value of the input state from X/MAX's perspective.
        Legal terminal utilities are -1, 0, and +1.

    action:
        Optimal action selected at the INPUT state.
        Use None if the input state is terminal.

        Tie-breaking rule:
        If multiple actions have the same optimal value, keep the first action
        returned by game.actions(state).

    nodes_visited:
        Number of states entered by the recursive search.
        Count the root, internal states, and terminal states.

    terminal_evaluations:
        Number of terminal states whose utility is evaluated.

    cutoffs:
        Number of actual Alpha-Beta pruning events.

        Count a cutoff only when alpha >= beta causes the algorithm to stop
        BEFORE examining all remaining actions at that node.

        For ordinary Minimax, this must be 0.
    """

    value: int
    action: Action | None
    nodes_visited: int
    terminal_evaluations: int
    cutoffs: int


def minimax(game: TicTacToe, state: State) -> SearchResult:
    """
    Compute the exact Minimax value and optimal action for state.

    Requirements
    ------------
    - Search all the way to terminal states.
    - X is MAX and O is MIN.
    - Terminal states return game.utility(state).
    - MAX nodes choose the child with the largest value.
    - MIN nodes choose the child with the smallest value.
    - Preserve the action order returned by game.actions(state).
    - For equal-valued actions, keep the first action in that order.
    - Do not use Alpha-Beta pruning in this function.
    - Do not use caching, depth limits, or heuristic evaluation.
    - Correctly report nodes_visited and terminal_evaluations.
    - Return cutoffs=0.

    You may add private helper functions above or below this function.

    TODO: Implement this function.
    """
    raise NotImplementedError("TODO: implement minimax")


def alphabeta(game: TicTacToe, state: State) -> SearchResult:
    """
    Compute the exact Minimax value and optimal action using Alpha-Beta pruning.

    Requirements
    ------------
    - Search all the way to terminal states except where Alpha-Beta proves
      that remaining branches cannot affect the result.
    - X is MAX and O is MIN.
    - Start the root search with alpha = -infinity and beta = +infinity.
    - At MAX nodes, update alpha using the best value found so far.
    - At MIN nodes, update beta using the best value found so far.
    - Prune when alpha >= beta.
    - Preserve the action order returned by game.actions(state).
    - For equal-valued actions, keep the first action in that order.
    - Return the SAME value and selected action as minimax(game, state).
    - Do not use caching, depth limits, or heuristic evaluation.
    - Correctly report nodes_visited, terminal_evaluations, and cutoffs.

    You may add private helper functions above or below this function.

    TODO: Implement this function.
    """
    raise NotImplementedError("TODO: implement alphabeta")
