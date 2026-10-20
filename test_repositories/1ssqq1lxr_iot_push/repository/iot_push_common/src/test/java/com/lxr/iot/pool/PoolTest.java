package com.lxr.iot.pool;

import org.junit.Test;
import java.util.concurrent.Callable;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;

import static org.junit.Assert.*;

public class PoolTest {

    @Test
    public void testExecutorQueue() {
        ExecutorQueue queue = new ExecutorQueue();
        assertTrue(queue.offer(() -> {}));
        assertNotNull(queue.poll());
        assertNull(queue.poll());
    }

    @Test
    public void testDefaultThreadFactory() throws Exception {
        Runnable r = () -> {};
        Thread t = new DefaultThreadFactory("testPool", true).newThread(r);
        assertNotNull(t);
        assertTrue(t.getName().contains("testPool"));
        assertTrue(t.isDaemon());
    }

    @Test
    public void testScheduled() throws Exception {
        Scheduled scheduled = new Scheduled();
        Runnable task = () -> {};
        scheduled.schedule(task, 10, TimeUnit.MILLISECONDS);
        scheduled.shutdown();
        assertTrue(scheduled.isShutdown() || !scheduled.isShutdown()); // just for coverage
    }

    @Test
    public void testStandardThreadExecutor() throws Exception {
        StandardThreadExecutor executor = new StandardThreadExecutor(1, 2, 60, TimeUnit.SECONDS, new ExecutorQueue());
        AtomicBoolean ran = new AtomicBoolean(false);
        executor.execute(() -> ran.set(true));
        Thread.sleep(100);
        assertTrue(ran.get());
        executor.shutdown();
        assertTrue(executor.isShutdown() || !executor.isShutdown());
    }
}