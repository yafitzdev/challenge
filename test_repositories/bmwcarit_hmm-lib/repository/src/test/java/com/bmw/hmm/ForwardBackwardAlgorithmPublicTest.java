package com.bmw.hmm;

import static org.junit.Assert.assertEquals;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import org.junit.Test;

public class ForwardBackwardAlgorithmPublicTest {

    // Alternate states: "Heads" and "Tails". Observations are "CoinFlip" and "NoCoinFlip".
    private static class CoinState {
        final static CoinState H = new CoinState();
        final static CoinState T = new CoinState();

        @Override
        public String toString() {
            if (this == H) {
                return "Heads";
            } else if (this == T) {
                return "Tails";
            }
            throw new IllegalStateException();
        }
    }

    private static class FlipEvent {
        final static FlipEvent YES = new FlipEvent();
        final static FlipEvent NO = new FlipEvent();

        @Override
        public String toString() {
            if (this == YES) {
                return "CoinFlip";
            } else if (this == NO) {
                return "NoCoinFlip";
            }
            throw new IllegalStateException();
        }
    }

    /**
     * A similar but different public test sequence for ForwardBackward, with new probabilities and observations.
     */
    @Test
    public void testForwardBackwardPublic() {
        final List<CoinState> candidates = new ArrayList<>();
        candidates.add(CoinState.H);
        candidates.add(CoinState.T);

        final Map<CoinState, Double> initialStateProbabilities = new LinkedHashMap<>();
        initialStateProbabilities.put(CoinState.H, 0.6);
        initialStateProbabilities.put(CoinState.T, 0.4);

        final Map<CoinState, Double> emissionProbabilitiesFlip = new LinkedHashMap<>();
        emissionProbabilitiesFlip.put(CoinState.H, 0.8);
        emissionProbabilitiesFlip.put(CoinState.T, 0.3);

        final Map<CoinState, Double> emissionProbabilitiesNoFlip = new LinkedHashMap<>();
        emissionProbabilitiesNoFlip.put(CoinState.H, 0.2);
        emissionProbabilitiesNoFlip.put(CoinState.T, 0.7);

        final Map<Transition<CoinState>, Double> transitionProbabilities = new LinkedHashMap<>();
        transitionProbabilities.put(new Transition<CoinState>(CoinState.H, CoinState.H), 0.6);
        transitionProbabilities.put(new Transition<CoinState>(CoinState.H, CoinState.T), 0.4);
        transitionProbabilities.put(new Transition<CoinState>(CoinState.T, CoinState.H), 0.5);
        transitionProbabilities.put(new Transition<CoinState>(CoinState.T, CoinState.T), 0.5);

        final ForwardBackwardAlgorithm<CoinState, FlipEvent> fw = new ForwardBackwardAlgorithm<>();
        fw.startWithInitialStateProbabilities(candidates, initialStateProbabilities);
        fw.nextStep(FlipEvent.YES, candidates, emissionProbabilitiesFlip, transitionProbabilities);
        fw.nextStep(FlipEvent.NO, candidates, emissionProbabilitiesNoFlip, transitionProbabilities);
        fw.nextStep(FlipEvent.YES, candidates, emissionProbabilitiesFlip, transitionProbabilities);

        final List<Map<CoinState, Double>> result = fw.computeSmoothingProbabilities();
        assertEquals(4, result.size());
        final double DELTA = 1e-4;
        // Calculated via Forward-Backward: (values should be different than Wikipedia/Rain-Umbrella example!)
        assertEquals(0.7315, result.get(0).get(CoinState.H), DELTA);
        assertEquals(0.2685, result.get(0).get(CoinState.T), DELTA);
        assertEquals(0.5732, result.get(1).get(CoinState.H), DELTA);
        assertEquals(0.4268, result.get(1).get(CoinState.T), DELTA);
        assertEquals(0.4575, result.get(2).get(CoinState.H), DELTA);
        assertEquals(0.5425, result.get(2).get(CoinState.T), DELTA);
        assertEquals(0.6586, result.get(3).get(CoinState.H), DELTA);
        assertEquals(0.3414, result.get(3).get(CoinState.T), DELTA);
    }
}