"""Port of com.bmw.hmm.ViterbiAlgorithm."""
from .forward_backward_algorithm import ForwardBackwardAlgorithm
from .sequence_state import SequenceState
from .transition import Transition
from . import utils

NEGATIVE_INFINITY = float("-inf")


class _ExtendedState(object):
    def __init__(self, state, back_pointer, observation, transition_descriptor):
        self.state = state
        self.back_pointer = back_pointer
        self.observation = observation
        self.transition_descriptor = transition_descriptor


class _ForwardStepResult(object):
    def __init__(self):
        self.new_message = {}
        self.new_extended_states = {}


class ViterbiAlgorithm(object):
    def __init__(self):
        self._last_extended_states = None
        self._prev_candidates = None
        self._message = None
        self._is_broken = False
        self._forward_backward = None
        self._message_history = None

    def setKeepMessageHistory(self, keep_message_history):
        if self.processingStarted():
            raise RuntimeError("Processing has already started.")
        self._message_history = [] if keep_message_history else None
        return self

    def setComputeSmoothingProbabilities(self, compute_smoothing_probabilities):
        if self.processingStarted():
            raise RuntimeError("Processing has already started.")
        self._forward_backward = ForwardBackwardAlgorithm() if compute_smoothing_probabilities else None
        return self

    def processingStarted(self):
        return self._message is not None

    def startWithInitialStateProbabilities(self, initial_states, initial_log_probabilities):
        self._initialize_state_probabilities(None, initial_states, initial_log_probabilities)
        if self._forward_backward is not None:
            self._forward_backward.start_with_initial_state_probabilities(
                initial_states, utils.log_to_non_log_probabilities(initial_log_probabilities))

    def startWithInitialObservation(self, observation, candidates, emission_log_probabilities):
        self._initialize_state_probabilities(observation, candidates, emission_log_probabilities)
        if self._forward_backward is not None:
            self._forward_backward.start_with_initial_observation(
                observation, candidates,
                utils.log_to_non_log_probabilities(emission_log_probabilities))

    def nextStep(self, observation, candidates, emission_log_probabilities,
                 transition_log_probabilities, transition_descriptors=None):
        """transition_descriptors=None corresponds to the Java overload without descriptors
        (an empty map)."""
        if transition_descriptors is None:
            transition_descriptors = {}
        if not self.processingStarted():
            raise RuntimeError("startWithInitialStateProbabilities() or startWithInitialObservation() "
                               "must be called first.")
        if self._is_broken:
            raise RuntimeError("Method must not be called after an HMM break.")

        result = self._forward_step(observation, self._prev_candidates, candidates, self._message,
                                    emission_log_probabilities, transition_log_probabilities,
                                    transition_descriptors)
        self._is_broken = self._hmm_break(result.new_message)
        if self._is_broken:
            return
        if self._message_history is not None:
            self._message_history.append(result.new_message)
        self._message = result.new_message
        self._last_extended_states = result.new_extended_states
        self._prev_candidates = list(candidates)

        if self._forward_backward is not None:
            self._forward_backward.next_step(
                observation, candidates,
                utils.log_to_non_log_probabilities(emission_log_probabilities),
                utils.log_to_non_log_probabilities(transition_log_probabilities))

    def computeMostLikelySequence(self):
        if self._message is None:
            return []
        return self._retrieve_most_likely_sequence()

    def isBroken(self):
        return self._is_broken

    def isComputeSmoothingProbabilities(self):
        return self._forward_backward is not None

    def isKeepMessageHistory(self):
        return self._message_history is not None

    def messageHistory(self):
        return self._message_history

    def messageHistoryString(self):
        if self._message_history is None:
            raise RuntimeError("Message history was not recorded.")
        sb = ["Message history with log probabilies\n\n"]
        for i, message in enumerate(self._message_history):
            sb.append("Time step " + str(i) + "\n")
            for state in message:
                sb.append(str(state) + ": " + str(message[state]) + "\n")
            sb.append("\n")
        return "".join(sb)

    # snake_case aliases
    set_keep_message_history = setKeepMessageHistory
    set_compute_smoothing_probabilities = setComputeSmoothingProbabilities
    processing_started = processingStarted
    start_with_initial_state_probabilities = startWithInitialStateProbabilities
    start_with_initial_observation = startWithInitialObservation
    next_step = nextStep
    compute_most_likely_sequence = computeMostLikelySequence
    is_broken = isBroken
    is_compute_smoothing_probabilities = isComputeSmoothingProbabilities
    is_keep_message_history = isKeepMessageHistory
    message_history = messageHistory
    message_history_string = messageHistoryString

    @staticmethod
    def _hmm_break(message):
        for log_probability in message.values():
            if log_probability != NEGATIVE_INFINITY:
                return False
        return True

    def _initialize_state_probabilities(self, observation, candidates, initial_log_probabilities):
        if self.processingStarted():
            raise RuntimeError("Initial probabilities have already been set.")
        initial_message = {}
        for candidate in candidates:
            log_probability = initial_log_probabilities.get(candidate)
            if log_probability is None:
                raise TypeError("No initial probability for " + str(candidate))
            initial_message[candidate] = log_probability
        self._is_broken = self._hmm_break(initial_message)
        if self._is_broken:
            return
        self._message = initial_message
        if self._message_history is not None:
            self._message_history.append(self._message)
        self._last_extended_states = {}
        for candidate in candidates:
            self._last_extended_states[candidate] = _ExtendedState(candidate, None, observation, None)
        self._prev_candidates = list(candidates)

    def _forward_step(self, observation, prev_candidates, cur_candidates, message,
                      emission_log_probabilities, transition_log_probabilities,
                      transition_descriptors):
        result = _ForwardStepResult()
        assert len(prev_candidates) > 0
        for cur_state in cur_candidates:
            max_log_probability = NEGATIVE_INFINITY
            max_prev_state = None
            found = False
            for prev_state in prev_candidates:
                log_probability = message[prev_state] + self._transition_log_probability(
                    prev_state, cur_state, transition_log_probabilities)
                if log_probability > max_log_probability:
                    max_log_probability = log_probability
                    max_prev_state = prev_state
                    found = True
            emission = emission_log_probabilities[cur_state]
            if emission is None:
                raise TypeError("No emission probability for " + str(cur_state))
            result.new_message[cur_state] = max_log_probability + emission
            if found:
                transition = Transition(max_prev_state, cur_state)
                result.new_extended_states[cur_state] = _ExtendedState(
                    cur_state, self._last_extended_states.get(max_prev_state), observation,
                    transition_descriptors.get(transition))
        return result

    @staticmethod
    def _transition_log_probability(prev_state, cur_state, transition_log_probabilities):
        p = transition_log_probabilities.get(Transition(prev_state, cur_state))
        return NEGATIVE_INFINITY if p is None else p

    def _most_likely_state(self):
        assert len(self._message) > 0
        result = None
        found = False
        max_log_probability = NEGATIVE_INFINITY
        for state, value in self._message.items():
            if value > max_log_probability:
                result = state
                max_log_probability = value
                found = True
        assert found
        return result

    def _retrieve_most_likely_sequence(self):
        assert len(self._message) > 0
        last_state = self._most_likely_state()
        result = []
        es = self._last_extended_states.get(last_state)
        smoothing = None
        if self._forward_backward is not None:
            smoothing = self._forward_backward.compute_smoothing_probabilities()
        idx = len(smoothing) if smoothing is not None else 0
        while es is not None:
            if self._forward_backward is not None:
                assert idx > 0
                idx -= 1
                smoothing_probability = smoothing[idx].get(es.state)
            else:
                smoothing_probability = None
            result.append(SequenceState(es.state, es.observation, es.transition_descriptor,
                                        smoothing_probability))
            es = es.back_pointer
        result.reverse()
        return result
