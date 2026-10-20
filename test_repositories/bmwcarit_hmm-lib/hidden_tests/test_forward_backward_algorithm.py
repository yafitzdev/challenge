from bmwcarit_hmm.forward_backward_algorithm import ForwardBackwardAlgorithm
from bmwcarit_hmm.transition import Transition

class Rain:
    T = object()
    F = object()

    def __str__(self):
        if self is Rain.T:
            return "Rain"
        elif self is Rain.F:
            return "Sun"
        raise RuntimeError("Unknown Rain object")

Rain.T = Rain()
Rain.F = Rain()

class Umbrella:
    T = object()
    F = object()

    def __str__(self):
        if self is Umbrella.T:
            return "Umbrella"
        elif self is Umbrella.F:
            return "No umbrella"
        raise RuntimeError("Unknown Umbrella object")

Umbrella.T = Umbrella()
Umbrella.F = Umbrella()

def test_forward_backward():
    candidates = [Rain.T, Rain.F]

    initial_state_probabilities = {Rain.T: 0.5, Rain.F: 0.5}

    emission_probabilities_umbrella = {Rain.T: 0.9, Rain.F: 0.2}
    emission_probabilities_no_umbrella = {Rain.T: 0.1, Rain.F: 0.8}

    transition_probabilities = {}
    transition_probabilities[Transition(Rain.T, Rain.T)] = 0.7
    transition_probabilities[Transition(Rain.T, Rain.F)] = 0.3
    transition_probabilities[Transition(Rain.F, Rain.T)] = 0.3
    transition_probabilities[Transition(Rain.F, Rain.F)] = 0.7

    fw = ForwardBackwardAlgorithm()
    fw.start_with_initial_state_probabilities(candidates, initial_state_probabilities)
    fw.next_step(Umbrella.T, candidates, emission_probabilities_umbrella, transition_probabilities)
    fw.next_step(Umbrella.T, candidates, emission_probabilities_umbrella, transition_probabilities)
    fw.next_step(Umbrella.F, candidates, emission_probabilities_no_umbrella, transition_probabilities)
    fw.next_step(Umbrella.T, candidates, emission_probabilities_umbrella, transition_probabilities)
    fw.next_step(Umbrella.T, candidates, emission_probabilities_umbrella, transition_probabilities)
    result = fw.compute_smoothing_probabilities()
    assert len(result) == 6
    DELTA = 1e-4
    assert abs(result[0][Rain.T] - 0.6469) < DELTA
    assert abs(result[0][Rain.F] - 0.3531) < DELTA
    assert abs(result[1][Rain.T] - 0.8673) < DELTA
    assert abs(result[1][Rain.F] - 0.1327) < DELTA
    assert abs(result[2][Rain.T] - 0.8204) < DELTA
    assert abs(result[2][Rain.F] - 0.1796) < DELTA
    assert abs(result[3][Rain.T] - 0.3075) < DELTA
    assert abs(result[3][Rain.F] - 0.6925) < DELTA
    assert abs(result[4][Rain.T] - 0.8204) < DELTA
    assert abs(result[4][Rain.F] - 0.1796) < DELTA
    assert abs(result[5][Rain.T] - 0.8673) < DELTA
    assert abs(result[5][Rain.F] - 0.1327) < DELTA