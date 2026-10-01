# Programming Lab 2 — Experimental Analysis

**Name:** Maddox Guthrie \
**CWID:** 12184185 \
**Section:** CS-565-001

---

## Experiment 1 — Position A

Run:

```bash
python run_search.py --position a --algorithm all
```

| Algorithm | Minimax Value | Selected Action | Nodes Visited | Terminal Evaluations | Cutoffs |
|---|---:|---:|---:|---:|---:|
| Minimax | 1 | 2 | 157 | 73 | 0 |
| Alpha-Beta | 1 | 2 | 36 | 13 | 16 |

### Brief observation

Both methods returned the value 1 and action 2. Alpha-Beta did so with a 77% reduction in nodes visited,
from 157 down to just 36.
Because the winning move is the first one tried, $\alpha$ becomes the highest possible value,
causing the remaining moves to be pruned almost immediately.
Minimax must traverse the entire game tree even if a winning move has already been found.

---

## Experiment 2 — Position C

Run:

```bash
python run_search.py --position c --algorithm all
```

| Algorithm | Minimax Value | Selected Action | Nodes Visited | Terminal Evaluations | Cutoffs |
|---|---:|---:|---:|---:|---:|
| Minimax | -1 | 7 | 38 | 17 | 0 |
| Alpha-Beta | -1 | 7 | 29 | 13 | 1 |

### Brief observation

Position C resulted in the same value of -1 and action of 7 for both approaches.
For this position Alpha-Beta only improved the number of nodes visited by 24%, from 38 down to 29.
This is expected, since the winning move is tried third, so O had to look at 2 non-winning moves first, and the tree was already small.
In this case Minimax doesn't do much extra work compared to Alpha-Beta.

---

## Experiment 3 — Empty Board

Run:

```bash
python run_search.py --position empty --algorithm all
```

| Algorithm | Minimax Value | Selected Action | Nodes Visited | Terminal Evaluations | Cutoffs |
|---|---:|---:|---:|---:|---:|
| Minimax | 0 | 0 | 549946 | 255168 | 0 |
| Alpha-Beta | 0 | 0 | 18297 | 7330 | 4237 |

### Search reduction

Use the following formula:

$$
\text{Reduction}
=
\left(
1 -
\frac{N_{\alpha\beta}}
     {N_{\text{Minimax}}}
\right)
\times 100\%
$$

**Percentage reduction in nodes visited:**

$$
\text{Reduction}
=
\left(
1 -
\frac{18297}
     {549946}
\right)
\times 100\%
=
96.672
$$

---

# Analysis Questions

## Question 1

Across the tested positions, did Minimax and Alpha-Beta return the same
minimax value and selected action? Why should this happen?

**Answer:**
Yes, both algorithms returned the same value and action in every position.
This happens because Alpha-Beta only skips branches that cannot affect the value at the root.
So it'll find the same value, and since the order is kept and ties keep the first action, the selected action is the same too.

## Question 2

Consider this partial game tree:

```text
              MAX
             /   \
           MIN   MIN
          /  \   / | \
         3   5  2  ?  ?
```

After the left MIN subtree returns 3:

1. What is $\alpha$ at the root?
2. After the first explored child of the right MIN node returns 2, what is $\beta$ at that MIN node?
3. Why can the two remaining children be pruned?

**Answer:**
1. 3
2. 2
3. $\alpha (3) \ge \beta (2)$, so the other 2 children can be pruned.
The right MIN node can be worth at most 2, and since MAX already has 3 from the left side,
it would never pick this branch regardless of what the remaining children are.


## Question 3

Alpha-Beta has the same worst-case asymptotic time complexity as Minimax.
Why can it still examine far fewer states in practice?

**Answer:**
In the worst case the best move is found last.
This means Alpha-Beta will still have to look at every node, just like Minimax.
Both are $O(b^d)$ in this case.
In practice, good moves are often found earlier, so many branches are pruned.
This can be seen in the empty board example where Alpha-Beta only visited 18,297 nodes instead of 549,946.

## Question 4

Why can the order in which legal actions are explored affect the amount of
Alpha-Beta pruning even though it does not change the final minimax value?

**Answer:**
The final minimax value is the same no matter what order it explores.
This is because Alpha-Beta only skips branches that can't change it.
Pruning depends on how fast $\alpha$ and $\beta$ get tight.
If a strong move is explored early, the bounds tighten quickly.
If it is explored late, the bounds stay loose for far longer, so very few branches are pruned.
For example in Question 2, the 2 let us prune the other children of the right MIN node because MAX already had 3 from the left branch.
If the 3 was found later, there would be no bound to prune against, so the right branch would have been explored.