from bmwcarit_hmm.sequence_state import SequenceState

def test_sequence_state_fields():
    state = "state_1"
    observation = 42
    transition_desc = "desc"
    smoothing = 0.5

    seq_state = SequenceState(state, observation, transition_desc, smoothing)
    assert seq_state.state == state
    assert seq_state.observation == observation
    assert seq_state.transition_descriptor == transition_desc
    assert seq_state.smoothing_probability == smoothing

def test_sequence_state_nulls():
    seq_state = SequenceState("state", None, None, None)
    assert seq_state.state == "state"
    assert seq_state.observation is None
    assert seq_state.transition_descriptor is None
    assert seq_state.smoothing_probability is None