package com.github.gcacace.signaturepad.utils;

import org.junit.Test;

import static org.junit.Assert.*;

public class TimedPointTest {

    @Test
    public void testSet() {
        TimedPoint tp = new TimedPoint();
        assertSame(tp, tp.set(5, 10));
        assertEquals(5, tp.x, 0.01);
        assertEquals(10, tp.y, 0.01);
    }

    @Test
    public void testDistanceTo() {
        TimedPoint t1 = new TimedPoint().set(0, 0);
        TimedPoint t2 = new TimedPoint().set(3, 4);
        float dist = t1.distanceTo(t2);
        assertEquals(5.0, dist, 0.001);
    }

    @Test
    public void testVelocityFromPositiveDiff() throws InterruptedException {
        TimedPoint t1 = new TimedPoint().set(0, 0);
        Thread.sleep(2); // Small delay
        TimedPoint t2 = new TimedPoint().set(3, 4);
        float velocity = t2.velocityFrom(t1);
        assertTrue(velocity > 0);
    }

    @Test
    public void testVelocityFromZeroDiff() {
        TimedPoint t1 = new TimedPoint().set(0, 0);
        TimedPoint t2 = new TimedPoint();
        t2.x = 3; t2.y = 4; t2.timestamp = t1.timestamp; // same timestamp as t1
        float velocity = t2.velocityFrom(t1);
        assertEquals(5.0, velocity, 0.001);
    }

    @Test
    public void testVelocityNaNInfinite() {
        TimedPoint t1 = new TimedPoint();
        t1.x = t1.y = 0;
        t1.timestamp = 100;
        TimedPoint t2 = new TimedPoint();
        t2.x = t2.y = 0;
        t2.timestamp = 200;
        float velocity = t2.velocityFrom(t1); // distance is 0 -> velocity 0
        assertEquals(0, velocity, 0.0);
    }
}