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

from grid import GridProblem, State

from collections import deque
import heapq

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

    reconstructed_path: list[State] = []
    cur = goal
    while True:
        if cur is None:
            break
        reconstructed_path.append(cur)
        cur = came_from[cur]
    reconstructed_path.reverse()
    return reconstructed_path


def bfs(problem: GridProblem) -> SearchResult:
    start: State = problem.start
    goal: State = problem.goal
    frontier: deque[State] = deque([start])
    visited: set[State] = {start}
    came_from: dict[State, State | None] = {start: None}
    nodes_expanded: int = 0
    found: bool = False

    while frontier:
        cur_state: State = frontier.popleft()
        if problem.is_goal(cur_state):
            found = True
            break

        for neighbor in problem.neighbors(cur_state):
            if neighbor not in visited:
                visited.add(neighbor)
                frontier.append(neighbor)
                came_from[neighbor] = cur_state
        nodes_expanded += 1

    if not found:
        return SearchResult.failure(nodes_expanded)

    path: list[State] = _reconstruct_path(came_from, start, goal)
    cost: float | int = problem.path_cost(path)
    return SearchResult(path, cost, nodes_expanded)


def ucs(problem: GridProblem) -> SearchResult:
    start: State = problem.start
    goal: State = problem.goal
    counter: int = 0
    frontier: list[tuple[int, int, State]] = [(0, counter, start)]
    counter += 1
    heapq.heapify(frontier)
    came_from: dict[State, State | None] = {start: None}
    g_cost: dict[State, int] = {start: 0}
    nodes_expanded: int = 0
    found: bool = False

    while frontier:
        g_val, _, cur_state = heapq.heappop(frontier)

        if cur_state in g_cost and g_cost[cur_state] < g_val:
            continue

        if problem.is_goal(cur_state):
            found = True
            break

        for neighbor in problem.neighbors(cur_state):
            tentative_g = g_cost[cur_state] + problem.step_cost(neighbor)
            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                heapq.heappush(frontier, (tentative_g, counter, neighbor))
                came_from[neighbor] = cur_state
                counter += 1
        nodes_expanded += 1

    if not found:
        return SearchResult.failure(nodes_expanded)

    path: list[State] = _reconstruct_path(came_from, start, goal)
    cost: float | int = problem.path_cost(path)
    return SearchResult(path, cost, nodes_expanded)


def manhattan(state: State, goal: State) -> int:
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])


def astar(problem: GridProblem) -> SearchResult:
    start: State = problem.start
    goal: State = problem.goal
    counter: int = 0
    s_heuristic: int = manhattan(start, goal)
    frontier: list[tuple[int, int, State]] = [(s_heuristic, counter, start)]
    counter += 1
    heapq.heapify(frontier)
    came_from: dict[State, State | None] = {start: None}
    g_cost: dict[State, int] = {start: 0}
    f_cost: dict[State, int] = {start: s_heuristic}
    nodes_expanded: int = 0
    found: bool = False

    while frontier:
        f_val, _, cur_state = heapq.heappop(frontier)

        if cur_state in f_cost and f_cost[cur_state] < f_val:
            continue

        if problem.is_goal(cur_state):
            found = True
            break

        for neighbor in problem.neighbors(cur_state):
            tentative_g = g_cost[cur_state] + problem.step_cost(neighbor)
            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                f_cost[neighbor] = tentative_g + manhattan(neighbor, goal)
                heapq.heappush(frontier, (f_cost[neighbor], counter, neighbor))
                came_from[neighbor] = cur_state
                counter += 1
        nodes_expanded += 1

    if not found:
        return SearchResult.failure(nodes_expanded)

    path: list[State] = _reconstruct_path(came_from, start, goal)
    cost: float | int = problem.path_cost(path)
    return SearchResult(path, cost, nodes_expanded)
