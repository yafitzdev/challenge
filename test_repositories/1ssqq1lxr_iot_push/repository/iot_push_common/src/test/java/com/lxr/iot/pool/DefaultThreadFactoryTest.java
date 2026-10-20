package com.lxr.iot.pool;

import org.junit.Test;

import java.util.concurrent.ThreadFactory;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.Assert.*;

public class DefaultThreadFactoryTest {

    @Test
    public void testNewThread() throws InterruptedException {
        DefaultThreadFactory factory = new DefaultThreadFactory("test");
        AtomicReference<Thread> threadRef = new AtomicReference<>();
        Runnable r = () -> threadRef.set(Thread.currentThread());

        Thread t = factory.newThread(r);
        t.start();
        t.join();

        assertNotNull(threadRef.get());
        assertTrue(threadRef.get().getName().startsWith("test-"));
    }
}