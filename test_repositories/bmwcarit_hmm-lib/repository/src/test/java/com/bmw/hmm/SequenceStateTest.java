package com.bmw.hmm;

import org.junit.Test;
import static org.junit.Assert.*;

public class SequenceStateTest {

    @Test
    public void testSequenceStateFields() {
        String state = "state_1";
        Integer observation = 42;
        String transitionDesc = "desc";
        Double smoothing = 0.5;

        SequenceState<String, Integer, String> seqState = new SequenceState<>(state, observation, transitionDesc, smoothing);

        assertEquals(state, seqState.state);
        assertEquals(observation, seqState.observation);
        assertEquals(transitionDesc, seqState.transitionDescriptor);
        assertEquals(smoothing, seqState.smoothingProbability);
    }

    @Test
    public void testSequenceStateNulls() {
        SequenceState<String, Integer, String> seqState = new SequenceState<>("state", null, null, null);

        assertEquals("state", seqState.state);
        assertNull(seqState.observation);
        assertNull(seqState.transitionDescriptor);
        assertNull(seqState.smoothingProbability);
    }
}