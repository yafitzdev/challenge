package com.github.gcacace.signaturepad.utils;

import org.junit.Test;
import static org.junit.Assert.*;

public class BezierTest {

    @Test
    public void testSetAndPoint() {
        TimedPoint sp = new TimedPoint().set(0, 0);
        TimedPoint c1 = new TimedPoint().set(5, 5);
        TimedPoint c2 = new TimedPoint().set(10, 5);
        TimedPoint ep = new TimedPoint().set(10, 0);
        Bezier bezier = new Bezier();
        bezier.set(sp, c1, c2, ep);
        assertEquals(sp, bezier.startPoint);
        assertEquals(c1, bezier.control1);
        assertEquals(c2, bezier.control2);
        assertEquals(ep, bezier.endPoint);

        double pointX = bezier.point(0.5f, 0, 5, 10, 10);
        assertTrue(pointX > 0);
        assertTrue(pointX < 10);

        double pointY = bezier.point(0.5f, 0, 5, 5, 0);
        assertTrue(pointY >= 0 && pointY <= 5);
    }

    @Test
    public void testLengthStraightLine() {
        TimedPoint sp = new TimedPoint().set(0, 0);
        TimedPoint c1 = new TimedPoint().set(0, 0);
        TimedPoint c2 = new TimedPoint().set(10, 0);
        TimedPoint ep = new TimedPoint().set(10, 0);
        Bezier bezier = new Bezier();
        bezier.set(sp, c1, c2, ep);
        float length = bezier.length();
        assertTrue("Length should be about 10, got: " + length, length > 9 && length < 11);
    }

    @Test
    public void testLengthCurved() {
        TimedPoint sp = new TimedPoint().set(0, 0);
        TimedPoint c1 = new TimedPoint().set(0, 10);
        TimedPoint c2 = new TimedPoint().set(10, 10);
        TimedPoint ep = new TimedPoint().set(10, 0);
        Bezier bezier = new Bezier();
        bezier.set(sp, c1, c2, ep);
        float length = bezier.length();
        // Should be longer than the straight line
        assertTrue(length > 10);
    }
}