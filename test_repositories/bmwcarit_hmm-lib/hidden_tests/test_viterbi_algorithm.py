import pytest
import math
from bmwcarit_hmm.transition import Transition
from bmwcarit_hmm.sequence_state import SequenceState
from bmwcarit_hmm.viterbi_algorithm import ViterbiAlgorithm

class Rain:
    pass
Rain.T = Rain()
Rain.F = Rain()

def rain_str(self):
    if self is Rain.T:
        return "Rain"
    elif self is Rain.F:
        return "Sun"
    raise RuntimeError()
Rain.__str__ = rain_str

class Umbrella:
    pass
Umbrella.T = Umbrella()
Umbrella.F = Umbrella()

def umbrella_str(self):
    if self is Umbrella.T:
        return "Umbrella"
    elif self is Umbrella.F:
        return "No umbrella"
    raise RuntimeError()
Umbrella.__str__ = umbrella_str

class Descriptor:
    pass
Descriptor.R2R = Descriptor()
Descriptor.R2S = Descriptor()
Descriptor.S2R = Descriptor()
Descriptor.S2S = Descriptor()

def descriptor_str(self):
    if self is Descriptor.R2R:
        return "R2R"
    elif self is Descriptor.R2S:
        return "R2S"
    elif self is Descriptor.S2R:
        return "S2R"
    elif self is Descriptor.S2S:
        return "S2S"
    raise RuntimeError()
Descriptor.__str__ = descriptor_str

DELTA = 1e-8

def states(sequence_states):
    return [ss.state for ss in sequence_states]

def test_compute_most_likely_sequence():
    candidates = [Rain.T, Rain.F]
    emission_log_probs_umbrella = {Rain.T: math.log(0.9), Rain.F: math.log(0.2)}
    emission_log_probs_no_umbrella = {Rain.T: math.log(0.1), Rain.F: math.log(0.8)}
    transition_log_probs = {
        Transition(Rain.T, Rain.T): math.log(0.7),
        Transition(Rain.T, Rain.F): math.log(0.3),
        Transition(Rain.F, Rain.T): math.log(0.3),
        Transition(Rain.F, Rain.F): math.log(0.7)
    }
    transition_descriptors = {
        Transition(Rain.T, Rain.T): Descriptor.R2R,
        Transition(Rain.T, Rain.F): Descriptor.R2S,
        Transition(Rain.F, Rain.T): Descriptor.S2R,
        Transition(Rain.F, Rain.F): Descriptor.S2S
    }
    viterbi = ViterbiAlgorithm().setKeepMessageHistory(True).setComputeSmoothingProbabilities(True)
    viterbi.startWithInitialObservation(Umbrella.T, candidates, emission_log_probs_umbrella)
    viterbi.nextStep(Umbrella.T, candidates, emission_log_probs_umbrella, transition_log_probs, transition_descriptors)
    viterbi.nextStep(Umbrella.F, candidates, emission_log_probs_no_umbrella, transition_log_probs, transition_descriptors)
    viterbi.nextStep(Umbrella.T, candidates, emission_log_probs_umbrella, transition_log_probs, transition_descriptors)

    result = viterbi.computeMostLikelySequence()
    assert len(result) == 4
    assert result[0].state == Rain.T
    assert result[1].state == Rain.T
    assert result[2].state == Rain.F
    assert result[3].state == Rain.T

def test_set_params():
    viterbi = ViterbiAlgorithm()
    assert not viterbi.isKeepMessageHistory()
    viterbi.setKeepMessageHistory(True)
    assert viterbi.isKeepMessageHistory()
    viterbi.setKeepMessageHistory(False)
    assert not viterbi.isKeepMessageHistory()

    assert not viterbi.isComputeSmoothingProbabilities()
    viterbi.setComputeSmoothingProbabilities(True)
    assert viterbi.isComputeSmoothingProbabilities()
    viterbi.setComputeSmoothingProbabilities(False)
    assert not viterbi.isComputeSmoothingProbabilities()

# Additional tests for edge cases can also be added here, following the Java original closely.
# For brevity and clarity, only a few illustrations provided.