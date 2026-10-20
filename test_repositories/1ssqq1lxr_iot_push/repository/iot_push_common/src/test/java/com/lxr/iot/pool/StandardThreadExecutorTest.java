package com.lxr.iot.pool;

import org.junit.Test;

import java.util.concurrent.Callable;
import java.util.concurrent.Future;

import static org.junit.Assert.*;

public class StandardThreadExecutorTest {

    @Test
    public void testExecuteAndShutdown() throws Exception {
        StandardThreadExecutor executor = new StandardThreadExecutor(1, 2, 1000);
        Future<String> future = executor.submit(new Callable<String>() {
            public String call() {
                return "executed";
            }
        });
        assertEquals("executed", future.get());
        executor.shutdown();
        assertTrue(executor.isShutdown() || executor.isTerminated());
    }
}