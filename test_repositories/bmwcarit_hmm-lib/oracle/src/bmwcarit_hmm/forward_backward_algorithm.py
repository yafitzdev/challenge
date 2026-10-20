"""Port of com.bmw.hmm.ForwardBackwardAlgorithm."""
import math

from .transition import Transition
from . import utils


class _Step(object):
    def __init__(self, candidates, emission_probabilities, transition_probabilities,
                 forward_probabilities, scaling_divisor):
        self.candidates = candidates
        self.emission_probabilities = emission_probabilities
        self.transition_probabilities = transition_probabilities
        self.forward_probabilities = forward_probabilities
        self.scaling_divisor = scaling_divisor


class ForwardBackwardAlgorithm(object):
    DELTA = 1e-8

    def __init__(self):
        self._steps = None
        self._prev_candidates = None

    def start_with_initial_state_probabilities(self, initial_states, initial_probabilities):
        if not self._sums_to_one(initial_probabilities.values()):
            raise ValueError("Initial state probabilities must sum to 1.")
        self._initialize_state_probabilities(None, initial_states, initial_probabilities)

    def start_with_initial_observation(self, observation, candidates, emission_probabilities):
        self._initialize_state_probabilities(observation, candidates, emission_probabilities)

    def next_step(self, observation, candidates, emission_probabilities, transition_probabilities):
        if self._steps is None:
            raise RuntimeError("startWithInitialStateProbabilities(...) or "
                               "startWithInitialObservation(...) must be called first.")
        candidates = list(candidates)
        emission_probabilities = dict(emission_probabilities)
        transition_probabilities = dict(transition_probabilities)

        prev_forward = self._steps[-1].forward_probabilities
        cur_forward = {}
        total = 0.0
        for cur_state in candidates:
            fp = self._compute_forward_probability(cur_state, prev_forward,
                                                   emission_probabilities, transition_probabilities)
            cur_forward[cur_state] = fp
            total += fp
        self._normalize_forward_probabilities(cur_forward, total)
        self._steps.append(_Step(candidates, emission_probabilities, transition_probabilities,
                                 cur_forward, total))
        self._prev_candidates = candidates

    def compute_smoothing_probabilities(self, out_backward_probabilities=None):
        assert out_backward_probabilities is None or len(out_backward_probabilities) == 0
        result = []
        if not self._steps:
            return result
        idx = len(self._steps) - 1
        step = self._steps[idx]
        backward = {}
        for candidate in step.candidates:
            backward[candidate] = 1.0
        if out_backward_probabilities is not None:
            out_backward_probabilities.append(backward)
        result.append(self._compute_smoothing_probabilities_vector(
            step.candidates, step.forward_probabilities, backward))
        while idx > 0:
            next_step = step
            idx -= 1
            step = self._steps[idx]
            next_backward = backward
            backward = {}
            for candidate in step.candidates:
                probability = self._compute_unscaled_backward_probability(
                    candidate, next_backward, next_step) / next_step.scaling_divisor
                backward[candidate] = probability
            if out_backward_probabilities is not None:
                out_backward_probabilities.append(backward)
            result.append(self._compute_smoothing_probabilities_vector(
                step.candidates, step.forward_probabilities, backward))
        result.reverse()
        return result

    def forward_probability(self, t, candidate):
        if self._steps is None:
            raise RuntimeError("No time steps yet.")
        return self._steps[t].forward_probabilities[candidate]

    def current_forward_probability(self, candidate):
        if self._steps is None:
            raise RuntimeError("No time steps yet.")
        return self.forward_probability(len(self._steps) - 1, candidate)

    def observation_log_probability(self):
        if self._steps is None:
            raise RuntimeError("No time steps yet.")
        result = 0.0
        for step in self._steps:
            result += math.log(step.scaling_divisor)
        return result

    # Java-style aliases
    startWithInitialStateProbabilities = start_with_initial_state_probabilities
    startWithInitialObservation = start_with_initial_observation
    nextStep = next_step
    computeSmoothingProbabilities = compute_smoothing_probabilities
    forwardProbability = forward_probability
    currentForwardProbability = current_forward_probability
    observationLogProbability = observation_log_probability

    def _compute_smoothing_probabilities_vector(self, candidates, forward, backward):
        assert len(forward) == len(backward)
        result = {}
        for state in candidates:
            probability = forward[state] * backward[state]
            assert utils.probability_in_range(probability, self.DELTA)
            result[state] = probability
        assert self._sums_to_one(result.values())
        return result

    def _compute_unscaled_backward_probability(self, candidate, next_backward, next_step):
        result = 0.0
        for next_candidate in next_step.candidates:
            result += next_step.emission_probabilities[next_candidate] * \
                next_backward[next_candidate] * \
                self._transition_probability(candidate, next_candidate,
                                             next_step.transition_probabilities)
        return result

    def _sums_to_one(self, probabilities):
        total = 0.0
        for p in probabilities:
            total += p
        return abs(total - 1.0) <= self.DELTA

    def _initialize_state_probabilities(self, observation, candidates, initial_probabilities):
        if self._steps is not None:
            raise RuntimeError("Initial probabilities have already been set.")
        candidates = list(candidates)
        self._steps = []
        forward = {}
        total = 0.0
        for candidate in candidates:
            fp = initial_probabilities[candidate]
            if fp is None:
                raise TypeError("No initial probability for " + str(candidate))
            forward[candidate] = fp
            total += fp
        self._normalize_forward_probabilities(forward, total)
        self._steps.append(_Step(candidates, None, None, forward, total))
        self._prev_candidates = candidates

    def _compute_forward_probability(self, cur_state, prev_forward, emission_probabilities,
                                     transition_probabilities):
        result = 0.0
        for prev_state in self._prev_candidates:
            result += prev_forward[prev_state] * self._transition_probability(
                prev_state, cur_state, transition_probabilities)
        result *= emission_probabilities[cur_state]
        return result

    @staticmethod
    def _transition_probability(prev_state, cur_state, transition_probabilities):
        p = transition_probabilities.get(Transition(prev_state, cur_state))
        return 0.0 if p is None else p

    @staticmethod
    def _normalize_forward_probabilities(forward, total):
        for key in list(forward.keys()):
            forward[key] = forward[key] / total
