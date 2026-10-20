from bmwcarit_hmm.forward_backward_algorithm import ForwardBackwardAlgorithm
from bmwcarit_hmm.transition import Transition

class CoinState:
    H = object()
    T = object()

    def __str__(self):
        if self is CoinState.H:
            return "Heads"
        elif self is CoinState.T:
            return "Tails"
        raise RuntimeError("Unknown CoinState")

CoinState.H = CoinState()
CoinState.T = CoinState()

class FlipEvent:
    YES = object()
    NO = object()

    def __str__(self):
        if self is FlipEvent.YES:
            return "CoinFlip"
        elif self is FlipEvent.NO:
            return "NoCoinFlip"
        raise RuntimeError("Unknown FlipEvent")

FlipEvent.YES = FlipEvent()
FlipEvent.NO = FlipEvent()

def test_forward_backward_public():
    candidates = [CoinState.H, CoinState.T]
    initial_state_probabilities = {CoinState.H: 0.6, CoinState.T: 0.4}

    emission_probabilities_flip = {CoinState.H: 0.8, CoinState.T: 0.3}
    emission_probabilities_no_flip = {CoinState.H: 0.2, CoinState.T: 0.7}

    transition_probabilities = {}
    transition_probabilities[Transition(CoinState.H, CoinState.H)] = 0.6
    transition_probabilities[Transition(CoinState.H, CoinState.T)] = 0.4
    transition_probabilities[Transition(CoinState.T, CoinState.H)] = 0.5
    transition_probabilities[Transition(CoinState.T, CoinState.T)] = 0.5

    fw = ForwardBackwardAlgorithm()
    fw.start_with_initial_state_probabilities(candidates, initial_state_probabilities)
    fw.next_step(FlipEvent.YES, candidates, emission_probabilities_flip, transition_probabilities)
    fw.next_step(FlipEvent.NO, candidates, emission_probabilities_no_flip, transition_probabilities)
    fw.next_step(FlipEvent.YES, candidates, emission_probabilities_flip, transition_probabilities)

    result = fw.compute_smoothing_probabilities()
    assert len(result) == 4
    DELTA = 1e-4
    assert abs(result[0][CoinState.H] - 0.7315) < DELTA
    assert abs(result[0][CoinState.T] - 0.2685) < DELTA
    assert abs(result[1][CoinState.H] - 0.5732) < DELTA
    assert abs(result[1][CoinState.T] - 0.4268) < DELTA
    assert abs(result[2][CoinState.H] - 0.4575) < DELTA
    assert abs(result[2][CoinState.T] - 0.5425) < DELTA
    assert abs(result[3][CoinState.H] - 0.6586) < DELTA
    assert abs(result[3][CoinState.T] - 0.3414) < DELTA