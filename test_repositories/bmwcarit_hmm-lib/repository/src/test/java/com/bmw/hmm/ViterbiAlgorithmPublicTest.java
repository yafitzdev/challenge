package com.bmw.hmm;

import org.junit.Test;
import java.util.*;
import static org.junit.Assert.*;

public class ViterbiAlgorithmPublicTest {

    static final String S1 = "X";
    static final String S2 = "Y";
    static final String S3 = "Z";

    @Test
    public void testSimpleMostLikelySequencePublic() {
        List<String> states = Arrays.asList(S1, S2, S3);

        Map<String, Double> initialProbs = new LinkedHashMap<>();
        initialProbs.put(S1, 0.3);
        initialProbs.put(S2, 0.6);
        initialProbs.put(S3, 0.1);

        Map<Transition<String>, Double> transitions = new HashMap<>();
        transitions.put(new Transition<>(S1, S1), 0.5);
        transitions.put(new Transition<>(S1, S2), 0.2);
        transitions.put(new Transition<>(S1, S3), 0.3);
        transitions.put(new Transition<>(S2, S1), 0.1);
        transitions.put(new Transition<>(S2, S2), 0.7);
        transitions.put(new Transition<>(S2, S3), 0.2);
        transitions.put(new Transition<>(S3, S1), 0.4);
        transitions.put(new Transition<>(S3, S2), 0.3);
        transitions.put(new Transition<>(S3, S3), 0.3);

        Map<String, Double> emission1 = new HashMap<>();
        emission1.put(S1, 0.5);
        emission1.put(S2, 0.4);
        emission1.put(S3, 0.1);

        Map<String, Double> emission2 = new HashMap<>();
        emission2.put(S1, 0.1);
        emission2.put(S2, 0.8);
        emission2.put(S3, 0.1);

        Map<String, Double> emission3 = new HashMap<>();
        emission3.put(S1, 0.6);
        emission3.put(S2, 0.3);
        emission3.put(S3, 0.1);

        List<String> observations = Arrays.asList("ObsA", "ObsB", "ObsC");
        List<Map<String, Double>> emissions = Arrays.asList(emission1, emission2, emission3);

        ViterbiAlgorithm<String, String> viterbi = new ViterbiAlgorithm<>();
        viterbi.startWithInitialStateProbabilities(states, initialProbs);

        for(int i=0; i<observations.size(); i++) {
            viterbi.nextStep(observations.get(i), states, emissions.get(i), transitions, "t"+i);
        }

        List<SequenceState<String, String, String>> result = viterbi.computeMostLikelySequence();
        assertEquals(4, result.size());
        assertEquals(S2, result.get(0).state);
        assertEquals(S2, result.get(1).state);
        assertEquals(S2, result.get(2).state);
        assertEquals(S2, result.get(3).state);
    }

    @Test
    public void testNullTransitionDescriptorPublic() {
        List<String> states = Arrays.asList(S1, S2);

        Map<String, Double> initialProbs = new HashMap<>();
        initialProbs.put(S1, 0.5);
        initialProbs.put(S2, 0.5);

        Map<Transition<String>, Double> transitions = new HashMap<>();
        transitions.put(new Transition<>(S1, S1), 0.5);
        transitions.put(new Transition<>(S1, S2), 0.5);
        transitions.put(new Transition<>(S2, S1), 0.5);
        transitions.put(new Transition<>(S2, S2), 0.5);

        Map<String, Double> emission1 = new HashMap<>();
        emission1.put(S1, 1.0);
        emission1.put(S2, 0.0);

        ViterbiAlgorithm<String, Integer> viterbi = new ViterbiAlgorithm<>();
        viterbi.startWithInitialStateProbabilities(states, initialProbs);
        viterbi.nextStep(1, states, emission1, transitions, null);

        List<SequenceState<String, Integer, ?>> result = viterbi.computeMostLikelySequence();
        assertNull(result.get(1).transitionDescriptor);
    }
}