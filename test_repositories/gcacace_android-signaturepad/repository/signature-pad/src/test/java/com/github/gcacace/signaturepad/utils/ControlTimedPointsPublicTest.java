package com.github.gcacace.signaturepad.utils;

import org.junit.Test;

import static org.junit.Assert.*;

public class ControlTimedPointsPublicTest {

    @Test
    public void testSetWithDifferentPoints() {
        TimedPoint c1 = new TimedPoint().set(-5.5, 42.42);
        TimedPoint c2 = new TimedPoint().set(100, -200);
        ControlTimedPoints control = new ControlTimedPoints();
        assertSame(control, control.set(c1, c2));
        assertEquals(c1, control.c1);
        assertEquals(c2, control.c2);
    }
}