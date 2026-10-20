package com.tuenti.smsradar;

import org.junit.Test;
import static org.junit.Assert.*;

public class TimeProviderTest {
    @Test
    public void testNowReturnsCurrentTime() {
        TimeProvider provider = new TimeProvider();
        long before = System.currentTimeMillis();
        long now = provider.now();
        long after = System.currentTimeMillis();
        assertTrue(now >= before && now <= after);
    }
}