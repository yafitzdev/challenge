class SequenceState(object):
    """State of the most likely sequence with additional information."""

    def __init__(self, state, observation, transition_descriptor, smoothing_probability):
        self.state = state
        self.observation = observation
        self.transition_descriptor = transition_descriptor
        self.smoothing_probability = smoothing_probability

    @property
    def transitionDescriptor(self):
        return self.transition_descriptor

    @property
    def smoothingProbability(self):
        return self.smoothing_probability
