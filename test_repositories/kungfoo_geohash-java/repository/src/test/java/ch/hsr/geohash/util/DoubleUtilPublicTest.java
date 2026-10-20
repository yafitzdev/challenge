package ch.hsr.geohash.util;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

public class DoubleUtilPublicTest {

    @Test
    public void testPositiveValue_public() {
        assertEquals(27.0, DoubleUtil.remainderWithFix(27.0, 360), 0.00001);
        assertEquals(199.5, DoubleUtil.remainderWithFix(919.5, 360), 0.00001);
    }

    @Test
    public void testNegativeValue_public() {
        assertEquals(320.2, DoubleUtil.remainderWithFix(-39.8, 360), 0.00001);
        assertEquals(111.1, DoubleUtil.remainderWithFix(-248.9, 360), 0.00001);
    }
}