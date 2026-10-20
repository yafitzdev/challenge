from bmwcarit_hmm.transition import Transition
from bmwcarit_hmm.viterbi_algorithm import ViterbiAlgorithm
from bmwcarit_hmm.sequence_state import SequenceState

S1 = "X"
S2 = "Y"
S3 = "Z"

def test_simple_most_likely_sequence_public():
    states = [S1, S2, S3]

    initial_probs = {S1: 0.3, S2: 0.6, S3: 0.1}
    transitions = {
        Transition(S1, S1): 0.5,
        Transition(S1, S2): 0.2,
        Transition(S1, S3): 0.3,
        Transition(S2, S1): 0.1,
        Transition(S2, S2): 0.7,
        Transition(S2, S3): 0.2,
        Transition(S3, S1): 0.4,
        Transition(S3, S2): 0.3,
        Transition(S3, S3): 0.3,
    }
    emission1 = {S1: 0.5, S2: 0.4, S3: 0.1}
    emission2 = {S1: 0.1, S2: 0.8, S3: 0.1}
    emission3 = {S1: 0.6, S2: 0.3, S3: 0.1}
    observations = ["ObsA", "ObsB", "ObsC"]
    emissions = [emission1, emission2, emission3]

    viterbi = ViterbiAlgorithm()
    viterbi.startWithInitialStateProbabilities(states, initial_probs)

    for i in range(len(observations)):
        viterbi.nextStep(observations[i], states, emissions[i], transitions, f"t{i}")

    result = viterbi.computeMostLikelySequence()
    assert len(result) == 4
    assert result[0].state == S2
    assert result[1].state == S2
    assert result[2].state == S2
    assert result[3].state == S2

def test_null_transition_descriptor_public():
    states = [S1, S2]
    initial_probs = {S1: 0.5, S2: 0.5}
    transitions = {
        Transition(S1, S1): 0.5,
        Transition(S1, S2): 0.5,
        Transition(S2, S1): 0.5,
        Transition(S2, S2): 0.5
    }
    emission1 = {S1: 1.0, S2: 0.0}

    viterbi = ViterbiAlgorithm()
    viterbi.startWithInitialStateProbabilities(states, initial_probs)
    viterbi.nextStep(1, states, emission1, transitions, None)
    result = viterbi.computeMostLikelySequence()
    assert result[1].transition_descriptor is None