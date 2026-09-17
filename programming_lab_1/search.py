"""
search.py
Programming Lab 1 — Search Algorithms for Weighted Grid Navigation

THIS IS THE MAIN FILE YOU WILL EDIT.

Implement:
    1. _reconstruct_path
    2. bfs
    3. ucs
    4. manhattan
    5. astar

Do not change the required function names or parameter lists.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import inf
from xxlimited_35 import Null

from grid import GridProblem, State


@dataclass
class SearchResult:
    """
    Standard result returned by every search algorithm.

    Attributes
    ----------
    path:
        Sequence of states from start through goal, including both endpoints.
        Use [] if no solution exists.

    cost:
        Total traversal cost of path.
        Use float("inf") if no solution exists.

    nodes_expanded:
        Number of states whose successors were generated.

        Important:
        - The goal is NOT counted if the algorithm stops immediately when the
          goal is removed from the frontier.
        - Stale priority-queue entries discarded without generating successors
          are NOT counted.
    """

    path: list[State]
    cost: float
    nodes_expanded: int

    @property
    def found(self) -> bool:
        """Return True if a solution path was found."""
        return bool(self.path)

    @property
    def steps(self) -> int:
        """Return the number of moves in the path."""
        return len(self.path) - 1 if self.path else 0

    @classmethod
    def failure(cls, nodes_expanded: int) -> "SearchResult":
        """Convenience constructor for an unsuccessful search."""
        return cls(path=[], cost=inf, nodes_expanded=nodes_expanded)


def _reconstruct_path(
    came_from: dict[State, State | None],
    start: State,
    goal: State,
) -> list[State]:
    """
    Reconstruct a path from start to goal using parent pointers.

    The returned path must include both start and goal.

    TODO: Implement this function.
    """
    raise NotImplementedError("TODO: implement _reconstruct_path")


def bfs(problem: GridProblem) -> SearchResult:
    """
    Breadth-First Search.

    Requirements
    ------------
    - Use a FIFO frontier.
    - Search by increasing path depth.
    - Do not use terrain costs to choose the next frontier state.
    - Avoid repeatedly discovering the same state.
    - Stop when the goal is removed from the frontier.
    - Report the ACTUAL traversal cost of the returned path.
    - Count expanded states exactly as defined in the assignment.

    Returns
    -------
    SearchResult
        path, total path cost, and number of expanded states.

    TODO: Implement this function.
    """
    raise NotImplementedError("TODO: implement bfs")


def ucs(problem: GridProblem) -> SearchResult:
    """
    Uniform Cost Search.

    Requirements
    ------------
    - Use heapq as a priority queue.
    - Priority is g(n).
    - Maintain the best known g-value for every discovered state.
    - If a cheaper path to a state is found, update it and push a new entry.
    - Ignore stale queue entries without counting them as expanded.
    - Break equal-priority ties by insertion order.
    - Stop when the goal is removed from the frontier with its best known cost.

    Suggested priority-queue entry:
        (priority, counter, state)

    Returns
    -------
    SearchResult
        path, optimal path cost, and number of expanded states.

    TODO: Implement this function.
    """
    raise NotImplementedError("TODO: implement ucs")


def manhattan(state: State, goal: State) -> int:
    """
    Return Manhattan distance between state and goal.

        h(n) = |row_n - row_goal| + |col_n - col_goal|

    TODO: Implement this function.
    """
    raise NotImplementedError("TODO: implement manhattan")


def astar(problem: GridProblem) -> SearchResult:
    """
    A* Search using Manhattan distance.

    Requirements
    ------------
    - Use heapq as a priority queue.
    - Priority is f(n) = g(n) + h(n).
    - Use manhattan(state, problem.goal) for h(n).
    - Maintain the best known g-value for every discovered state.
    - If a cheaper path to a state is found, update it and push a new entry.
    - Ignore stale queue entries without counting them as expanded.
    - Break equal-priority ties by insertion order.
    - Stop when the goal is removed from the frontier with its best known cost.

    Suggested priority-queue entry:
        (priority, counter, state)

    Returns
    -------
    SearchResult
        path, optimal path cost, and number of expanded states.

    TODO: Implement this function.
    """
    raise NotImplementedError("TODO: implement astar")
