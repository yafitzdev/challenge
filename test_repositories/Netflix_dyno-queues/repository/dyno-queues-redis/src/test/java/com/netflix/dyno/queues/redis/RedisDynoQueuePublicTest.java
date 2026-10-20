package com.netflix.dyno.queues.redis;

import org.junit.Test;

import static org.junit.Assert.*;

public class RedisDynoQueuePublicTest {

    @Test
    public void testQueueNameAndShardDifferentCase() {
        RedisDynoQueue queue = new RedisDynoQueue(null, "testPublicQueue", null, 10, 0, 100, 2, null, null, "PUB", 0L, false, null);
        assertEquals("testPublicQueue", queue.getName());
        assertEquals("PUB", queue.getUnAckShardName());
    }

    @Test
    public void testCreatedWithDifferentSettings() {
        RedisDynoQueue q = new RedisDynoQueue(null, "publicQ", null, 5, 3, 33, 5, null, null, "PUBSHARD", 1L, true, null);
        assertEquals(5, q.getMessageRefreshInterval());
        assertEquals(3, q.getUnackTime());
        assertEquals(33, q.getMessageTimeout());
        assertEquals("PUBSHARD", q.getUnAckShardName());
        assertTrue(q.isRequeueOnTimeout());
        assertEquals(1L, q.getRequeueCheckTimeoutMillis());
    }

    @Test
    public void testShardIdSet() {
        RedisDynoQueue queue = new RedisDynoQueue(null, "queuePub", null, 10, 0, 100, 2, null, null, "publicShard", 0L, false, null);
        assertEquals("publicShard", queue.getUnAckShardName());
    }
}