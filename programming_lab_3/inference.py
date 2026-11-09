"""Programming Lab 3 - implement HMM filtering and prediction here.

Use Python 3.10+. Only the Python standard library is needed for inference.
All distributions and returned beliefs are Python lists of floats.
T[i][j] = P(X_t=j | X_(t-1)=i); sensor[j][e] = P(E_t=e | X_t=j).
Inputs are valid finite distributions of compatible dimensions. Observation
indices are valid nonnegative integers; steps is a nonnegative integer.
Do not mutate any input. Do not round intermediate results or hard-code models.
"""


def predict(belief, transition):
    """Return a NEW list: the one-step prediction over all hidden states.

    Sum over previous states for each destination state. Support any positive
    number of states, including asymmetric transition models.
    """
    result = []
    n = len(belief)
    for j in range(n):
        i_sum = 0
        for i in range(n):
            i_sum += belief[i] * transition[i][j]
        result.append(i_sum)
    return result


def update(predicted_belief, observation, sensor):
    """Return a NEW normalized posterior after the indexed observation.

    Multiply each predicted state probability by sensor[state][observation].
    If the sum of these weights is zero, raise ValueError. Otherwise normalize.
    Do not treat a merely small positive total as zero.
    """
    n = len(predicted_belief)
    result = []
    total = 0
    for k in range(n):
        total += predicted_belief[k] * sensor[k][observation]
    if total == 0:
        raise ValueError("total cannot be 0")
    for j in range(n):
        result.append(predicted_belief[j] * sensor[j][observation] / total)
    return result


def filter_sequence(prior, observations, transition, sensor):
    """Return [b_1, ..., b_T], one NEW belief list per observation.

    prior is b_0; observations[0] is E_1. First predict X_1 from X_0,
    then incorporate E_1. Do this for every observation. Return [] for an
    empty sequence. Do not include prior in the result. Beliefs must not alias
    one another or any input. Propagate ValueError for impossible evidence.
    You may call predict and update.
    """
    result = []
    current = prior
    for e in observations:
        predicted = predict(current, transition)
        current = update(predicted, e, sensor)
        result.append(current)
    return result


def predict_steps(belief, transition, steps):
    """Return a NEW belief after exactly steps transitions, without evidence.

    Return only the final distribution, not a history. For steps=0 return a
    copy of belief. You may call predict. Do not apply the sensor model.
    """
    result = belief.copy()
    for _ in range(steps):
        result = predict(result, transition)
    return result
