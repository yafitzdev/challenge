package com.lxr.iot.pool;

import org.junit.Test;
import static org.junit.Assert.*;

public class ExecutorQueueTest {

    @Test
    public void testOfferAndPoll() {
        ExecutorQueue<Integer> queue = new ExecutorQueue<>();
        assertTrue(queue.offer(1));
        assertEquals(Integer.valueOf(1), queue.poll());
        assertNull(queue.poll());
    }

    @Test
    public void testMultipleOperations() {
        ExecutorQueue<String> queue = new ExecutorQueue<>();
        assertTrue(queue.offer("A"));
        assertTrue(queue.offer("B"));
        assertEquals("A", queue.poll());
        assertEquals("B", queue.poll());
        assertNull(queue.poll());
    }

    @Test
    public void testSizeIsEmpty() {
        ExecutorQueue<Double> queue = new ExecutorQueue<>();
        assertTrue(queue.isEmpty());
        queue.offer(2.5);
        assertFalse(queue.isEmpty());
        assertEquals(1, queue.size());
        queue.poll();
        assertTrue(queue.isEmpty());
        assertEquals(0, queue.size());
    }
}