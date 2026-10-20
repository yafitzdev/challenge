package com.netflix.dyno.queues;

import org.junit.Test;

import java.util.concurrent.TimeUnit;

import static org.junit.Assert.*;

public class MessageTest {

    @Test
    public void testDefaultConstructor() {
        Message msg = new Message();
        assertNull(msg.getId());
        assertNull(msg.getPayload());
        assertEquals(0, msg.getTimeout());
        assertEquals(0, msg.getPriority());
        assertNull(msg.getShard());
    }

    @Test
    public void testParameterizedConstructor() {
        Message msg = new Message("abc", "payload");
        assertEquals("abc", msg.getId());
        assertEquals("payload", msg.getPayload());
    }

    @Test
    public void testSettersAndGetters() {
        Message msg = new Message();
        msg.setId("xyz");
        msg.setPayload("p1");
        msg.setTimeout(5000L);
        msg.setPriority(10);
        msg.setShard("shardA");

        assertEquals("xyz", msg.getId());
        assertEquals("p1", msg.getPayload());
        assertEquals(5000L, msg.getTimeout());
        assertEquals(10, msg.getPriority());
        assertEquals("shardA", msg.getShard());
    }

    @Test
    public void testSetTimeoutWithTimeUnit() {
        Message msg = new Message();
        msg.setTimeout(2, TimeUnit.SECONDS);
        assertEquals(2000L, msg.getTimeout());
    }

    @Test(expected = IllegalArgumentException.class)
    public void testSetPriorityTooLow() {
        Message msg = new Message();
        msg.setPriority(-1);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testSetPriorityTooHigh() {
        Message msg = new Message();
        msg.setPriority(100);
    }

    @Test
    public void testSetPriorityBoundaryValues() {
        Message msg = new Message();
        msg.setPriority(0);
        assertEquals(0, msg.getPriority());
        msg.setPriority(99);
        assertEquals(99, msg.getPriority());
    }

    @Test
    public void testEqualsAndHashCode() {
        Message m1 = new Message("id1", "payload1");
        Message m2 = new Message("id1", "payload2");
        Message m3 = new Message("id2", "payload1");
        Message m4 = new Message(null, "payload3");
        Message m5 = new Message(null, "payload4");

        assertTrue(m1.equals(m2));
        assertEquals(m1.hashCode(), m2.hashCode());

        assertFalse(m1.equals(m3));
        assertNotEquals(m1.hashCode(), m3.hashCode());

        // compare with null, different type, itself
        assertFalse(m1.equals(null));
        assertFalse(m1.equals("string"));
        assertTrue(m1.equals(m1));

        // both ids null
        assertTrue(m4.equals(m5));
        assertEquals(m4.hashCode(), m5.hashCode());

        // only one id null
        assertFalse(m1.equals(m4));
        assertFalse(m4.equals(m1));
    }

    @Test
    public void testToString() {
        Message msg = new Message("idToStr", "payloadStr");
        msg.setPriority(7);
        msg.setTimeout(123L);
        String str = msg.toString();
        assertTrue(str.contains("idToStr"));
        assertTrue(str.contains("payloadStr"));
        assertTrue(str.contains("priority=7"));
        assertTrue(str.contains("timeout=123"));
    }
}