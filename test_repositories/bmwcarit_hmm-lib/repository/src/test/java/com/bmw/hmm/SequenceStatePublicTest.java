package com.bmw.hmm;

import org.junit.Test;
import static org.junit.Assert.*;

public class SequenceStatePublicTest {

    @Test
    public void testSequenceStateFieldsPublic() {
        String state = "state_2";
        Integer observation = 99;
        String transitionDesc = "public_desc";
        Double smoothing = 0.75;

        SequenceState<String, Integer, String> seqState = new SequenceState<>(state, observation, transitionDesc, smoothing);

        assertEquals(state, seqState.state);
        assertEquals(observation, seqState.observation);
        assertEquals(transitionDesc, seqState.transitionDescriptor);
        assertEquals(smoothing, seqState.smoothingProbability);
    }

    @Test
    public void testSequenceStateNullsPublic() {
        SequenceState<String, Integer, String> seqState = new SequenceState<>("public_state", null, null, null);

        assertEquals("public_state", seqState.state);
        assertNull(seqState.observation);
        assertNull(seqState.transitionDescriptor);
        assertNull(seqState.smoothingProbability);
    }
}