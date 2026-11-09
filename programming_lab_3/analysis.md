# Programming Lab 3 - Experimental Analysis

**Name:** Maddox Guthrie \
**CWID:** 12184185 \
**Section:**  CS-565-001

Use your own program's output. Round displayed probabilities to six decimal
places; do not round intermediate calculations. Each numbered response should
normally be 2-4 sentences and refer to a specific value or feature of your plots.

## Experiment 1 - Classroom sequence (8 points)

Run `python run_inference.py --model umbrella --sequence classroom`.

| Day | Observation | Predicted P(Rain) | Filtered P(Rain)  | Filtered P(NoRain) |
|-----|-------------|-------------------|-------------------|--------------------|
| 1   | U           | 0.500000          | 0.818182          | 0.181818           |
| 2   | U           | 0.627273          | 0.883357          | 0.116643           |
| 3   | N           | 0.653343          | 0.190668          | 0.809332           |

1. Why does the probability of rain fall on day 3 without becoming zero?

**Answer:** On day 3 there is no umbrella, and N is much more likely under no rain ($P(N \mid \text{NoRain}) = 0.8$) than under rain ($P(N \mid \text{Rain}) = 0.1$), so the update lowers rain from 0.653343 to 0.190668.
It doesn't reach zero because the sensor is noisy: people still sometimes skip the umbrella when it rains, so N is only weak evidence, not proof.
The prediction going into day 3 was also nonzero, so some rain probability always survives.

2. Explain the two contributions to the day-3 prediction before incorporating N.
   Distinguish a prediction from an observation update.

**Answer:** The day-3 prediction is $$P(\text{Rain}_3) = 0.7(0.883357) + 0.3(0.116643) = 0.618350 + 0.034993 = 0.653343,$$ where the first term is rain on day 2 staying rain and the second is no rain on day 2 turning into rain.
A prediction only pushes the old belief forward in time using the transition model, with no new evidence.
An observation update uses the sensor model to reweight that prediction by how likely N is in each state, then renormalizes, which is what takes 0.653343 down to 0.190668.

## Experiment 2 - Controlled model comparisons (14 points)

Run `python run_experiments.py`. Use `results/comparisons.csv` and the two PNGs.
Day 0 is the prior. U means an umbrella is present; N means no umbrella.

### 2A. Sensor reliability

The transition model is fixed. Compare `reliable` and `noisy`.

| Sequence       | Model    | Day 3 P(Rain) | Day 4 P(Rain) | Day 6 P(Rain) |
|----------------|----------|---------------|---------------|---------------|
| A: U U U U U U | reliable | 0.976935      | 0.976982      | 0.976984      |
| A: U U U U U U | noisy    | 0.651772      | 0.656899      | 0.659459      |
| B: U N U N U N | reliable | 0.907392      | 0.093813      | 0.093658      |
| B: U N U N U N | noisy    | 0.576355      | 0.429683      | 0.428242      |
| C: U U U N N N | reliable | 0.976935      | 0.105204      | 0.023169      |
| C: U U U N N N | noisy    | 0.651772      | 0.459731      | 0.356503      |

1. How does sensor reliability change the response to alternating observations
   in B and to the first N in C? Use numerical evidence from your results.

**Answer:** In B the reliable model swings hard between days 3 and 4, from 0.907392 down to 0.093813 (a change of about 0.81), while the noisy model only goes from 0.576355 to 0.429683 (about 0.15).
In the plot the reliable line zigzags between about 0.1 and 0.95 and the noisy one barely wiggles around 0.5.
On the first N in C, reliable falls from 0.976935 to 0.105204, but noisy only falls from 0.651772 to 0.459731.
A reliable sensor has a more extreme likelihood ratio, so each observation moves the belief much more.

### 2B. State persistence

The sensor model is fixed. Compare `persistent` and `weak`.

| Sequence       | Model            | Day 3 P(Rain) | Day 4 P(Rain) | Day 6 P(Rain) |
|----------------|------------------|---------------|---------------|---------------|
| A: U U U U U U | persistent       | 0.961140      | 0.967562      | 0.969279      |
| A: U U U U U U | weak             | 0.837376      | 0.837431      | 0.837434      |
| B: U N U N U N | persistent       | 0.681314      | 0.185113      | 0.146200      |
| B: U N U N U N | weak             | 0.794706      | 0.123313      | 0.123310      |
| C: U U U N N N | persistent       | 0.961140      | 0.453121      | 0.026300      |
| C: U U U N N N | weak             | 0.837376      | 0.125178      | 0.096133      |

2. In sequence C, compare the beliefs immediately before and after the first N.
   How does state persistence affect the influence of the preceding U observations?

**Answer:** For the persistent model the belief drops from 0.961140 to 0.453121 at the first N, while for the weak model it drops from 0.837376 to 0.125178.
With persistence the day-4 prediction is still high (about 0.868912), so the earlier U observations still carry a lot of weight and one N only brings the belief down part of the way.
In the weak model the prediction is only about 0.533738, so the old U's are mostly forgotten and the single N takes over.
This matches the plot, where the persistent curve declines gradually and the weak curve falls off a cliff on day 4.

3. Compare B and C on day 4 (both observe N). Explain why the current observation alone does not
   determine the posterior. Identify the role of both the prediction and likelihood.

**Answer:** Both sequences see N on day 4, but the persistent model gives 0.185113 in B and 0.453121 in C.
The posterior is proportional to prediction times likelihood, and the likelihood of N (0.1 for rain, 0.8 for no rain) is the same in both cases.
What differs is the prediction, about 0.645052 for rain in B and 0.868912 in C, because the history before day 4 is different.
So the posterior depends on what the model believed before the observation as well as on the observation itself.

Submit `sensor_comparison.png` and `transition_comparison.png` as separate files
alongside this report. Do not edit plotted values or replace them with reference
answers. The PNGs are generated by the supplied script after your code works.

## Experiment 3 - Prediction without new observations (8 points)

Use the day-3 posterior from Experiment 1 and `results/future_predictions.csv`.
Here k counts transitions AFTER day 3; the umbrella model is unchanged.

| k  | P(Rain on day 3+k given E_1:E_3) | P(NoRain on day 3+k given E_1:E_3) |
|----|----------------------------------|------------------------------------|
| 0  | 0.190668                         | 0.809332                           |
| 1  | 0.376267                         | 0.623733                           |
| 2  | 0.450507                         | 0.549493                           |
| 5  | 0.496832                         | 0.503168                           |
| 10 | 0.499968                         | 0.500032                           |

1. Why does the distribution change even though no new evidence arrives?

**Answer:** The weather itself keeps changing from day to day, so the belief has to keep moving even with no umbrella data.
Each step applies the transition model, which lets some of the 0.809332 no-rain mass flip to rain.
For example, $k=1$ gives $0.7(0.190668) + 0.3(0.809332) = 0.376267$.
Without any observation to sharpen it, the belief just gets more uncertain over time.

2. Why do these predictions approach 0.5 for this transition model? Is 0.5
   necessarily the limiting rain probability for an asymmetric two-state model?
   Give a short explanation; no general stationary-distribution proof is required.

**Answer:** This transition matrix is symmetric (stay with probability 0.7, switch with probability 0.3 from either state), so $(0.5, 0.5)$ maps to itself, and the gap from 0.5 shrinks by a factor of $0.7 - 0.3 = 0.4$ each step.
That fits the table: $0.190668 - 0.5 = -0.309332$ at $k=0$ becomes $-0.123733$ at $k=1$, and by $k=10$ it is only about $3 \times 10^{-5}$ away.
For an asymmetric model 0.5 is not necessarily the limit, since the belief heads toward that model's own stationary distribution.
For example, with $\begin{bmatrix} 0.9 & 0.1 \\ 0.4 & 0.6 \end{bmatrix}$ the limiting rain probability is 0.8, not 0.5.
