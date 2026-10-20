package com.bmw.hmm;

import org.junit.Test;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;

import static org.junit.Assert.*;

public class UtilsTest {

    @Test
    public void testInitialHashMapCapacity() {
        assertEquals(14, Utils.initialHashMapCapacity(10));
    }

    @Test
    public void testLogToNonLogProbabilities() {
        Map<String, Double> logProbs = new LinkedHashMap<>();
        logProbs.put("A", Math.log(0.4));
        logProbs.put("B", Math.log(0.6));
        Map<String, Double> probs = Utils.logToNonLogProbabilities(logProbs);
        assertEquals(0.4, probs.get("A"), 1e-10);
        assertEquals(0.6, probs.get("B"), 1e-10);
    }

    @Test
    public void testProbabilityInRange() {
        assertTrue(Utils.probabilityInRange(1.0, 1e-8));
        assertTrue(Utils.probabilityInRange(0.0, 1e-8));
        assertFalse(Utils.probabilityInRange(-0.01, 1e-4));
        assertTrue(Utils.probabilityInRange(1.000009, 1e-3));
        assertFalse(Utils.probabilityInRange(1.2, 1e-4));
    }
}