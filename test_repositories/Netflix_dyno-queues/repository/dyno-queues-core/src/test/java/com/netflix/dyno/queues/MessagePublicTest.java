package com.netflix.dyno.queues;

import org.junit.Test;

import java.util.concurrent.TimeUnit;

import static org.junit.Assert.*;

public class MessagePublicTest {

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
        Message msg = new Message("def", "data");
        assertEquals("def", msg.getId());
        assertEquals("data", msg.getPayload());
    }

    @Test
    public void testSettersAndGetters() {
        Message msg = new Message();
        msg.setId("uvw");
        msg.setPayload("payloadX");
        msg.setTimeout(12000L);
        msg.setPriority(5);
        msg.setShard("shardB");

        assertEquals("uvw", msg.getId());
        assertEquals("payloadX", msg.getPayload());
        assertEquals(12000L, msg.getTimeout());
        assertEquals(5, msg.getPriority());
        assertEquals("shardB", msg.getShard());
    }

    @Test
    public void testSetTimeoutWithTimeUnit() {
        Message msg = new Message();
        msg.setTimeout(3, TimeUnit.MINUTES);
        assertEquals(180000L, msg.getTimeout());
    }

    @Test(expected = IllegalArgumentException.class)
    public void testSetPriorityTooLow() {
        Message msg = new Message();
        msg.setPriority(-5);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testSetPriorityTooHigh() {
        Message msg = new Message();
        msg.setPriority(150);
    }

    @Test
    public void testSetPriorityBoundaryValues() {
        Message msg = new Message();
        msg.setPriority(1);
        assertEquals(1, msg.getPriority());
        msg.setPriority(98);
        assertEquals(98, msg.getPriority());
    }

    @Test
    public void testEqualsAndHashCode() {
        Message m1 = new Message("idX", "payload3");
        Message m2 = new Message("idX", "payload4");
        Message m3 = new Message("idY", "payload3");
        Message m4 = new Message(null, "payloadA");
        Message m5 = new Message(null, "payloadB");

        assertTrue(m1.equals(m2));
        assertEquals(m1.hashCode(), m2.hashCode());

        assertFalse(m1.equals(m3));
        assertNotEquals(m1.hashCode(), m3.hashCode());

        // compare with null, different type, itself
        assertFalse(m1.equals(null));
        assertFalse(m1.equals(new Object()));
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
        Message msg = new Message("idToString", "payloadTest");
        msg.setPriority(12);
        msg.setTimeout(999L);
        String str = msg.toString();
        assertTrue(str.contains("idToString"));
        assertTrue(str.contains("payloadTest"));
        assertTrue(str.contains("priority=12"));
        assertTrue(str.contains("timeout=999"));
    }
}