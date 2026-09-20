# Programming Lab 1 — Experimental Analysis

**Name:**  Maddox Guthrie \
**CWID:**  12184185 \
**Section:**  CS-565-001

---

## Experiment 1 — Uniform-Cost Grid (`maps/map1.txt`)

| Algorithm | Path Cost | Number of Steps | Nodes Expanded |
|---|---:|---:|---:|
| BFS | 11 | 11 | 25 |
| UCS | 11 | 11 | 25 |
| A* | 11 | 11 | 19 |

### Brief observation

BFS and UCS perform identically here. This makes sense given the nature of their respective algorithms.
BFS expands the frontier by distance (depth) from the start, and only continues to the next depth once all
current-depth nodes have been added to the frontier. UCS expands based on total path cost so far, so on a uniform-cost
map it expands away from the start the same way BFS does. A*, however, uses the heuristic to guide it, allowing it to
take a more direct route, which is why we see it expand fewer nodes.

---

## Experiment 2 — Weighted Grid (`maps/map2.txt`)

| Algorithm | Path Cost | Number of Steps | Nodes Expanded |
|---|---:|---:|---:|
| BFS | 57 | 8 | 15 |
| UCS | 12 | 12 | 13 |
| A* | 12 | 12 | 12 |

### Brief observation

BFS finds the shortest path, but has the most nodes expanded and the highest cost. This is because BFS does not consider
cost as a factor when expanding the frontier. UCS and A* do consider cost, so they avoid the short but vastly more
expensive row of 8s across the top of the grid. A* has one fewer expanded node because it never has to expand an 8 node,
whereas UCS will once the total cost of the path reaches 8, making the first 8 node the next cheapest.

---

## Experiment 3 — Heuristic Search (`maps/map3.txt`)

| Algorithm | Path Cost | Number of Steps | Nodes Expanded |
|---|---:|---:|---:|
| BFS | 28 | 28 | 336 |
| UCS | 28 | 28 | 336 |
| A* | 28 | 28 | 126 |

### Brief observation

While both UCS and A* find the same shortest path, the number of expanded nodes is widely different. UCS expands tiles
in all directions with no bias toward any direction. A*, in comparison, expands toward the goal, ignoring nodes that are
far out of the way or in the wrong direction.

---

# Analysis Questions

## Question 1

Why can BFS return a path with a higher total cost than UCS on a weighted grid?

**Answer:**
BFS ignores path costs and only expands the frontier based on path depth. Therefore, a shallower path, even one that is
vastly more expensive than any other path, is discovered first.

## Question 2

Suppose UCS and A* return paths with the same optimal cost, but A* expands fewer states. Why can this happen?


**Answer:** A* has the heuristic to guide it, allowing it to aim toward the goal state. Because A*'s priority is f(n) =
g(n) + h(n), a state that's cheap to reach but far from the goal (high h) gets pushed lower in priority. UCS's priority
is g(n) alone, so it has no way to know a state is "far from the goal" and might expand it purely because it's cheap so
far, even if it's a dead end or leads away from the solution.


## Question 3

What happens to A* if \(h(n)=0\) for every state? Explain using the A* evaluation function.

**Answer:** A* will behave exactly like UCS. Since h(n) = 0 for every state, the evaluation function \(f(n) = g(n) + 
h(n)\) reduces to \(f(n) = g(n)\), so path cost alone guides the algorithm's expansion, which is exactly how UCS operates.


## Question 4

Suppose Manhattan distance \(h(n)\) is replaced by \(h'(n)=2h(n)\). Is A* still guaranteed to return an optimal solution? Briefly explain.

**Answer:** No, A* is not guaranteed to return an optimal solution. A*'s optimality guarantee depends on the heuristic
being admissible, meaning h(n) never overestimates the true remaining cost to the goal. Manhattan distance is admissible
on this grid, but doubling it can push h'(n) past the true remaining cost at some states. Once the heuristic is
inadmissible, A* can settle on a state whose f-value looks low enough to seem best, when in fact a cheaper path was
still available but got deprioritized because its (accurate) heuristic estimate looked comparatively worse.
