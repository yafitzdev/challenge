package com.lxr.iot.pool;

import org.junit.Test;

import static org.junit.Assert.*;

public class ScheduledTest {

    @Test
    public void testScheduledRunnable() throws InterruptedException {
        Runnable task = () -> {};
        Scheduled scheduled = new Scheduled(task, 1000L);
        assertEquals(1000L, scheduled.getDelay());
        scheduled.setDelay(500L);
        assertEquals(500L, scheduled.getDelay());
    }
}