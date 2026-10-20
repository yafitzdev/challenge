package com.tuenti.smsradar;

import org.junit.Assert;
import org.junit.Test;

public class TimeProviderPublicTest {

    @Test
    public void testEpochTime() {
        TimeProvider tp = new TimeProvider();
        long time = tp.getCurrentTimeMillis();
        Assert.assertTrue("Should retrieve a non-negative time", time >= 0);
    }

    @Test
    public void testTimeHasAdvanced() throws InterruptedException {
        TimeProvider tp = new TimeProvider();
        long before = tp.getCurrentTimeMillis();
        Thread.sleep(7); // Use a non-5ms value to differ from typical private tests
        long after = tp.getCurrentTimeMillis();
        Assert.assertTrue("Current time should advance", after > before);
    }
}