"""
tic_tac_toe.py
Programming Lab 2 — Adversarial Search with Minimax and Alpha-Beta Pruning

This file is provided starter code.
Students should not modify this file.

Game conventions
----------------
X = MAX
O = MIN
X moves first.

Board indices:

    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8

Utility is defined from X/MAX's perspective:

    X win  -> +1
    draw   ->  0
    O win  -> -1

Legal actions are returned in ascending index order.
"""

from __future__ import annotations

State = tuple[str, ...]
Action = int

X = "X"
O = "O"
EMPTY = "."


class TicTacToe:
    """Deterministic, perfect-information 3x3 Tic-Tac-Toe."""

    _WINNING_LINES: tuple[tuple[int, int, int], ...] = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    )

    def __init__(self) -> None:
        self.initial_state: State = (EMPTY,) * 9

    def validate_state(self, state: State) -> None:
        """Raise ValueError if state violates the basic game conventions."""
        if len(state) != 9:
            raise ValueError("A Tic-Tac-Toe state must contain exactly 9 cells.")

        if any(cell not in {X, O, EMPTY} for cell in state):
            raise ValueError("Cells must be 'X', 'O', or '.'.")

        x_count = state.count(X)
        o_count = state.count(O)

        if x_count not in {o_count, o_count + 1}:
            raise ValueError(
                "Illegal move counts: X must have either the same number of "
                "moves as O or exactly one more."
            )

        winners = self._winning_players(state)

        if len(winners) > 1:
            raise ValueError("Illegal state: both X and O cannot be winners.")

        if X in winners and x_count != o_count + 1:
            raise ValueError("Illegal state: an X win must occur immediately after X moves.")

        if O in winners and x_count != o_count:
            raise ValueError("Illegal state: an O win must occur immediately after O moves.")

    def actions(self, state: State) -> list[Action]:
        """
        Return legal actions in the required fixed order: 0, 1, ..., 8.

        A terminal state has no legal actions.
        """
        self.validate_state(state)

        if self.terminal(state):
            return []

        return [index for index, cell in enumerate(state) if cell == EMPTY]

    def player(self, state: State) -> str:
        """Return the player whose turn it is: X (MAX) or O (MIN)."""
        self.validate_state(state)

        if self.terminal(state):
            raise ValueError("A terminal state has no player to move.")

        return X if state.count(X) == state.count(O) else O

    def result(self, state: State, action: Action) -> State:
        """Return the successor state produced by applying action."""
        self.validate_state(state)

        if self.terminal(state):
            raise ValueError("Cannot apply an action to a terminal state.")

        if not isinstance(action, int) or not 0 <= action <= 8:
            raise ValueError("Action must be an integer from 0 through 8.")

        if state[action] != EMPTY:
            raise ValueError(f"Square {action} is not empty.")

        next_state = list(state)
        next_state[action] = self.player(state)
        result_state = tuple(next_state)
        self.validate_state(result_state)
        return result_state

    def winner(self, state: State) -> str | None:
        """Return X, O, or None if there is currently no winner."""
        self.validate_state(state)
        winners = self._winning_players(state)
        return next(iter(winners)) if winners else None

    def terminal(self, state: State) -> bool:
        """Return True if the game is over."""
        # Avoid calling winner() here to keep validation recursion simple.
        winners = self._winning_players(state)
        return bool(winners) or EMPTY not in state

    def utility(self, state: State) -> int:
        """
        Return terminal utility from X/MAX's perspective.

        Raises
        ------
        ValueError
            If state is not terminal.
        """
        self.validate_state(state)

        if not self.terminal(state):
            raise ValueError("Utility is defined only for terminal states.")

        winner = self.winner(state)

        if winner == X:
            return 1
        if winner == O:
            return -1
        return 0

    def render(self, state: State) -> str:
        """Return a printable representation of the board."""
        self.validate_state(state)

        rows = []
        for start in (0, 3, 6):
            rows.append(" | ".join(state[start : start + 3]))

        return "\n---------\n".join(rows)

    def _winning_players(self, state: State) -> set[str]:
        """Return the set of players that currently have a winning line."""
        winners: set[str] = set()

        for a, b, c in self._WINNING_LINES:
            if state[a] != EMPTY and state[a] == state[b] == state[c]:
                winners.add(state[a])

        return winners


def state_from_string(text: str) -> State:
    """
    Convert a compact 9-character board string into a State.

    Example:
        "XX.OO...."
    """
    compact = "".join(text.split()).upper()

    if len(compact) != 9:
        raise ValueError("Board string must contain exactly 9 cells.")

    state = tuple(compact)
    TicTacToe().validate_state(state)
    return state
