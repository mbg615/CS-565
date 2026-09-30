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

from tic_tac_toe import Action, State, TicTacToe, X, O


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


def _minimax(game: TicTacToe, state: State, counters: list[int]):
    counters[0] += 1
    if game.terminal(state):
        counters[1] += 1
        return game.utility(state), None

    current_player = game.player(state)
    best_action = None

    if current_player == X:
        best_value = -float("inf")
    else:
        best_value = float("inf")

    for action in game.actions(state):
        child = game.result(state, action)
        child_val, _ = _minimax(game, child, counters)
        if current_player == X:
            if child_val > best_value:
                best_value = child_val
                best_action = action
        else:
            if child_val < best_value:
                best_value = child_val
                best_action = action

    return best_value, best_action


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

    """
    counters: list[int] = [0, 0]
    value, action = _minimax(game, state, counters)
    return SearchResult(value, action, counters[0], counters[1], 0)


def _alphabeta(game: TicTacToe, state: State, alpha: float, beta: float, counters: list[int]):
    counters[0] += 1
    if game.terminal(state):
        counters[1] += 1
        return game.utility(state), None

    current_player = game.player(state)
    best_action = None

    if current_player == X:
        best_value = -float("inf")
    else:
        best_value = float("inf")

    actions = game.actions(state)

    for i, action in enumerate(actions):
        child = game.result(state, action)
        child_val, _ = _alphabeta(game, child, alpha, beta ,counters)
        if current_player == X:
            if child_val > best_value:
                best_value = child_val
                alpha = max(alpha, best_value)
                best_action = action
        else:
            if child_val < best_value:
                best_value = child_val
                beta = min(beta, best_value)
                best_action = action

        if alpha >= beta:
            if i < len(actions) - 1:
                counters[2] += 1
            break

    return best_value, best_action

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
    """
    counters: list[int] = [0, 0, 0]
    value, action = _alphabeta(game, state, -float("inf"), float("inf"), counters)
    return SearchResult(value, action, counters[0], counters[1], counters[2])
