package com.github.gcacace.signaturepad.utils;

import org.junit.Test;

import static org.junit.Assert.*;

public class ControlTimedPointsTest {

    @Test
    public void testSet() {
        TimedPoint c1 = new TimedPoint().set(1, 2);
        TimedPoint c2 = new TimedPoint().set(3, 4);
        ControlTimedPoints control = new ControlTimedPoints();
        assertSame(control, control.set(c1, c2));
        assertEquals(c1, control.c1);
        assertEquals(c2, control.c2);
    }
}