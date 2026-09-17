"""
grid.py
Programming Lab 1 — Search Algorithms for Weighted Grid Navigation

This file is provided starter code.
Students should not modify this file.

Grid format
-----------
Each map is a whitespace-separated rectangular grid.

Allowed tokens:
    S   start state
    G   goal state
    #   obstacle
    1-9 positive traversal cost

Movement is limited to four directions in this fixed order:
    up, right, down, left

Path-cost convention:
    - The start state contributes cost 0.
    - Entering G costs 1.
    - Entering a numeric cell costs the integer shown in that cell.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

State = tuple[int, int]


class GridProblem:
    """A four-neighbor weighted grid-navigation problem."""

    _MOVES: tuple[tuple[int, int], ...] = (
        (-1, 0),  # up
        (0, 1),   # right
        (1, 0),   # down
        (0, -1),  # left
    )

    def __init__(self, grid: list[list[str]]):
        if not grid or not grid[0]:
            raise ValueError("Grid must contain at least one cell.")

        width = len(grid[0])
        if any(len(row) != width for row in grid):
            raise ValueError("Grid must be rectangular.")

        self.grid: tuple[tuple[str, ...], ...] = tuple(
            tuple(cell for cell in row) for row in grid
        )
        self.rows = len(self.grid)
        self.cols = width

        starts: list[State] = []
        goals: list[State] = []

        for r, row in enumerate(self.grid):
            for c, token in enumerate(row):
                if token == "S":
                    starts.append((r, c))
                elif token == "G":
                    goals.append((r, c))
                elif token == "#":
                    pass
                elif token.isdigit() and 1 <= int(token) <= 9:
                    pass
                else:
                    raise ValueError(
                        f"Invalid token {token!r} at row {r}, column {c}. "
                        "Use S, G, #, or an integer cost from 1 to 9."
                    )

        if len(starts) != 1:
            raise ValueError(f"Grid must contain exactly one S; found {len(starts)}.")
        if len(goals) != 1:
            raise ValueError(f"Grid must contain exactly one G; found {len(goals)}.")

        self.start: State = starts[0]
        self.goal: State = goals[0]

    @classmethod
    def from_file(cls, filename: str | Path) -> "GridProblem":
        """Load a whitespace-separated map file."""
        path = Path(filename)
        lines = [line.strip() for line in path.read_text().splitlines() if line.strip()]
        grid = [line.split() for line in lines]
        return cls(grid)

    def in_bounds(self, state: State) -> bool:
        """Return True if state lies inside the grid."""
        r, c = state
        return 0 <= r < self.rows and 0 <= c < self.cols

    def passable(self, state: State) -> bool:
        """Return True if state is not an obstacle."""
        if not self.in_bounds(state):
            return False
        r, c = state
        return self.grid[r][c] != "#"

    def is_goal(self, state: State) -> bool:
        """Return True if state is the goal."""
        return state == self.goal

    def neighbors(self, state: State) -> list[State]:
        """
        Return valid neighboring states in the required fixed order:

            up, right, down, left

        Students should not reorder this list.
        """
        r, c = state
        result: list[State] = []

        for dr, dc in self._MOVES:
            nxt = (r + dr, c + dc)
            if self.in_bounds(nxt) and self.passable(nxt):
                result.append(nxt)

        return result

    def step_cost(self, state: State) -> int:
        """
        Return the cost of ENTERING state.

        The start state has cost 0.
        The goal state has cost 1.
        Numeric terrain uses its displayed value.
        """
        if not self.in_bounds(state):
            raise ValueError(f"State {state} is outside the grid.")
        if not self.passable(state):
            raise ValueError(f"Obstacle state {state} has no traversal cost.")

        r, c = state
        token = self.grid[r][c]

        if token == "S":
            return 0
        if token == "G":
            return 1
        return int(token)

    def path_cost(self, path: Iterable[State]) -> float:
        """
        Compute total path cost using the assignment convention.

        The first state contributes zero cost; each later state contributes
        its entering cost. An empty path has infinite cost.
        """
        path_list = list(path)
        if not path_list:
            return float("inf")

        return float(sum(self.step_cost(state) for state in path_list[1:]))

    def validate_path(self, path: Iterable[State]) -> tuple[bool, str]:
        """Check whether a path is a valid start-to-goal path."""
        path_list = list(path)

        if not path_list:
            return False, "Path is empty."
        if path_list[0] != self.start:
            return False, f"Path must start at {self.start}."
        if path_list[-1] != self.goal:
            return False, f"Path must end at {self.goal}."

        for state in path_list:
            if not self.in_bounds(state):
                return False, f"State {state} is outside the grid."
            if not self.passable(state):
                return False, f"State {state} is an obstacle."

        for current, nxt in zip(path_list, path_list[1:]):
            if nxt not in self.neighbors(current):
                return False, f"Invalid move from {current} to {nxt}."

        return True, "Path is valid."

    def render(self, path: Iterable[State] | None = None) -> str:
        """
        Return a printable representation of the grid.

        If path is provided, intermediate path cells are shown as *.
        """
        path_states = set(path or [])
        rows: list[str] = []

        for r in range(self.rows):
            output_row: list[str] = []
            for c in range(self.cols):
                state = (r, c)
                token = self.grid[r][c]

                if state in path_states and token not in {"S", "G"}:
                    output_row.append("*")
                else:
                    output_row.append(token)

            rows.append(" ".join(output_row))

        return "\n".join(rows)
