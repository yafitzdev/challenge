package com.github.gcacace.signaturepad.utils;

import org.junit.Test;

import static org.junit.Assert.*;

public class TimedPointPublicTest {

    @Test
    public void testSetPublic() {
        TimedPoint tp = new TimedPoint();
        assertSame(tp, tp.set(-7.2, 8.19));
        assertEquals(-7.2, tp.x, 0.01);
        assertEquals(8.19, tp.y, 0.01);
    }

    @Test
    public void testDistanceToPublic() {
        TimedPoint t1 = new TimedPoint().set(1, 1);
        TimedPoint t2 = new TimedPoint().set(4, 5);
        float dist = t1.distanceTo(t2);
        assertEquals(5.0, dist, 0.001);
    }

    @Test
    public void testVelocityFromPositiveDiffPublic() throws InterruptedException {
        TimedPoint t1 = new TimedPoint().set(2, 3);
        Thread.sleep(2); // Small delay
        TimedPoint t2 = new TimedPoint().set(7, 11);
        float velocity = t2.velocityFrom(t1);
        assertTrue(velocity > 0);
    }

    @Test
    public void testVelocityFromZeroDiffPublic() {
        TimedPoint t1 = new TimedPoint().set(3, 4);
        TimedPoint t2 = new TimedPoint();
        t2.x = 6; t2.y = 8; t2.timestamp = t1.timestamp; // same timestamp as t1
        float velocity = t2.velocityFrom(t1);
        assertEquals(5.0, velocity, 0.001);
    }

    @Test
    public void testVelocityNaNInfinitePublic() {
        TimedPoint t1 = new TimedPoint();
        t1.x = t1.y = 10;
        t1.timestamp = 500;
        TimedPoint t2 = new TimedPoint();
        t2.x = t2.y = 10;
        t2.timestamp = 600;
        float velocity = t2.velocityFrom(t1); // distance is 0 -> velocity 0
        assertEquals(0, velocity, 0.0);
    }
}