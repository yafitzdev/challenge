package com.github.gcacace.signaturepad.utils;

import org.junit.Test;
import static org.junit.Assert.*;

public class BezierPublicTest {

    @Test
    public void testSetAndPointPublic() {
        TimedPoint sp = new TimedPoint().set(2, -2);
        TimedPoint c1 = new TimedPoint().set(4, 15);
        TimedPoint c2 = new TimedPoint().set(20, 10);
        TimedPoint ep = new TimedPoint().set(25, -4);
        Bezier bezier = new Bezier();
        bezier.set(sp, c1, c2, ep);
        assertEquals(sp, bezier.startPoint);
        assertEquals(c1, bezier.control1);
        assertEquals(c2, bezier.control2);
        assertEquals(ep, bezier.endPoint);

        double pointX = bezier.point(0.25f, 2, 4, 20, 25);
        assertTrue(pointX > 2 && pointX < 25);

        double pointY = bezier.point(0.75f, -2, 15, 10, -4);
        assertTrue(pointY > -4 && pointY < 15);
    }

    @Test
    public void testLengthDifferentStraightLine() {
        TimedPoint sp = new TimedPoint().set(10, 10);
        TimedPoint c1 = new TimedPoint().set(10, 10);
        TimedPoint c2 = new TimedPoint().set(30, 10);
        TimedPoint ep = new TimedPoint().set(30, 10);
        Bezier bezier = new Bezier();
        bezier.set(sp, c1, c2, ep);
        float length = bezier.length();
        assertTrue("Length should be about 20, got: " + length, length > 19 && length < 21);
    }

    @Test
    public void testLengthPublicCurved() {
        TimedPoint sp = new TimedPoint().set(5, 5);
        TimedPoint c1 = new TimedPoint().set(5, 25);
        TimedPoint c2 = new TimedPoint().set(25, 25);
        TimedPoint ep = new TimedPoint().set(25, 5);
        Bezier bezier = new Bezier();
        bezier.set(sp, c1, c2, ep);
        float length = bezier.length();
        assertTrue(length > 20);
    }
}