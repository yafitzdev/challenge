package com.lxr.iot.pool;

import org.junit.Test;
import static org.junit.Assert.*;

public class ExecutorQueuePublicTest {

    @Test
    public void testOfferAndPollWithDifferentValues() {
        ExecutorQueue<Integer> queue = new ExecutorQueue<>();
        assertTrue(queue.offer(99));
        assertEquals(Integer.valueOf(99), queue.poll());
        assertNull(queue.poll());
    }

    @Test
    public void testMultipleOperationsWithStrings() {
        ExecutorQueue<String> queue = new ExecutorQueue<>();
        assertTrue(queue.offer("X"));
        assertTrue(queue.offer("Y"));
        assertEquals("X", queue.poll());
        assertEquals("Y", queue.poll());
        assertNull(queue.poll());
    }

    @Test
    public void testSizeIsEmptyWithDifferentType() {
        ExecutorQueue<Double> queue = new ExecutorQueue<>();
        assertTrue(queue.isEmpty());
        queue.offer(7.7);
        assertFalse(queue.isEmpty());
        assertEquals(1, queue.size());
        queue.poll();
        assertTrue(queue.isEmpty());
        assertEquals(0, queue.size());
    }
}