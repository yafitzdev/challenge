package com.lxr.iot.pool;

import org.junit.Test;

import java.util.concurrent.ThreadFactory;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.Assert.*;

public class DefaultThreadFactoryPublicTest {

    @Test
    public void testNewThreadPublic() throws InterruptedException {
        DefaultThreadFactory factory = new DefaultThreadFactory("public-thread");
        AtomicReference<Thread> threadRef = new AtomicReference<>();
        Runnable r = () -> threadRef.set(Thread.currentThread());

        Thread t = factory.newThread(r);
        t.start();
        t.join();

        assertNotNull(threadRef.get());
        assertTrue(threadRef.get().getName().contains("public-thread"));
    }
}