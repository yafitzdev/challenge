from bmwcarit_hmm.sequence_state import SequenceState

def test_sequence_state_fields_public():
    state = "state_2"
    observation = 99
    transition_desc = "public_desc"
    smoothing = 0.75

    seq_state = SequenceState(state, observation, transition_desc, smoothing)
    assert seq_state.state == state
    assert seq_state.observation == observation
    assert seq_state.transition_descriptor == transition_desc
    assert seq_state.smoothing_probability == smoothing

def test_sequence_state_nulls_public():
    seq_state = SequenceState("public_state", None, None, None)
    assert seq_state.state == "public_state"
    assert seq_state.observation is None
    assert seq_state.transition_descriptor is None
    assert seq_state.smoothing_probability is None