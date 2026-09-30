# Programming Lab 2 — Experimental Analysis

**Name:**  
**CWID:**  
**Section:**  

---

## Experiment 1 — Position A

Run:

```bash
python run_search.py --position a --algorithm all
```

| Algorithm | Minimax Value | Selected Action | Nodes Visited | Terminal Evaluations | Cutoffs |
|---|---:|---:|---:|---:|---:|
| Minimax |  |  |  |  | 0 |
| Alpha-Beta |  |  |  |  |  |

### Brief observation

Write 2–4 sentences describing what you observe.

---

## Experiment 2 — Position C

Run:

```bash
python run_search.py --position c --algorithm all
```

| Algorithm | Minimax Value | Selected Action | Nodes Visited | Terminal Evaluations | Cutoffs |
|---|---:|---:|---:|---:|---:|
| Minimax |  |  |  |  | 0 |
| Alpha-Beta |  |  |  |  |  |

### Brief observation

Write 2–4 sentences describing what you observe.

---

## Experiment 3 — Empty Board

Run:

```bash
python run_search.py --position empty --algorithm all
```

| Algorithm | Minimax Value | Selected Action | Nodes Visited | Terminal Evaluations | Cutoffs |
|---|---:|---:|---:|---:|---:|
| Minimax |  |  |  |  | 0 |
| Alpha-Beta |  |  |  |  |  |

### Search reduction

Use the following formula:

\[
\text{Reduction}
=
\left(
1 -
\frac{N_{\alpha\beta}}
     {N_{\text{Minimax}}}
\right)
\times 100\%
\]

**Percentage reduction in nodes visited:**  

---

# Analysis Questions

## Question 1

Across the tested positions, did Minimax and Alpha-Beta return the same
minimax value and selected action? Why should this happen?

**Answer:**


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

1. What is \(\alpha\) at the root?
2. After the first explored child of the right MIN node returns 2, what is
   \(\beta\) at that MIN node?
3. Why can the two remaining children be pruned?

**Answer:**


## Question 3

Alpha-Beta has the same worst-case asymptotic time complexity as Minimax.
Why can it still examine far fewer states in practice?

**Answer:**


## Question 4

Why can the order in which legal actions are explored affect the amount of
Alpha-Beta pruning even though it does not change the final minimax value?

**Answer:**
