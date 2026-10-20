package com.bmw.hmm;

import org.junit.Test;
import java.util.*;
import static org.junit.Assert.*;

public class UtilsPublicTest {

    @Test
    public void testNormalizeProbabilitiesDifferent() {
        Map<String, Double> probs = new HashMap<>();
        probs.put("orange", 4.0);
        probs.put("banana", 6.0);

        Map<String, Double> norm = Utils.normalizeProbabilities(probs);

        assertEquals(0.4, norm.get("orange"), 1e-10);
        assertEquals(0.6, norm.get("banana"), 1e-10);

        // Original input is not modified
        assertEquals(4.0, probs.get("orange"), 1e-10);
        assertEquals(6.0, probs.get("banana"), 1e-10);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testNormalizeEmptyDifferent() {
        Utils.normalizeProbabilities(new HashMap<>());
    }

    @Test(expected = NullPointerException.class)
    public void testNormalizeNullValueDifferent() {
        Map<String, Double> p = new HashMap<>();
        p.put("something", null);
        Utils.normalizeProbabilities(p);
    }

    @Test
    public void testSumDifferentValues() {
        List<Double> l = Arrays.asList(2.5, 3.0, 7.5);
        assertEquals(13.0, Utils.sum(l), 1e-10);
    }

    @Test
    public void testLog2DifferentInputs() {
        assertEquals(1.0, Utils.log2(2.0), 1e-10);
        assertEquals(2.0, Utils.log2(4.0), 1e-10);
        assertEquals(0.0, Utils.log2(1.0), 1e-10);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testLog2ZeroDifferent() {
        Utils.log2(0.0);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testLog2NegativeDifferent() {
        Utils.log2(-2.0);
    }

    @Test
    public void testLogSumExpListDifferent() {
        List<Double> d = Arrays.asList(Math.log(2.0), Math.log(10.0));
        double expected = Math.log(2.0 + 10.0);
        assertEquals(expected, Utils.logSumExp(d), 1e-10);
    }

    @Test
    public void testLogSumExpArrayDifferent() {
        double[] arr = {Math.log(5), Math.log(3)};
        double expected = Math.log(5.0 + 3.0);
        assertEquals(expected, Utils.logSumExp(arr), 1e-10);
    }
}