package com.netflix.dyno.queues.redis.v2;

import org.junit.Test;

import static org.junit.Assert.*;

public class RedisDynoQueuePublicTest {

    @Test
    public void testQueueNameAndShardPublic() {
        RedisDynoQueue queue = new RedisDynoQueue(null, "queuePublicV2", null, 7, 1, 17, 2, null, null, "V2PUB", 10L, true, null);
        assertEquals("queuePublicV2", queue.getName());
        assertEquals("V2PUB", queue.getUnAckShardName());
    }

    @Test
    public void testDifferentSettingsPublic() {
        RedisDynoQueue q = new RedisDynoQueue(null, "queueV2Pub", null, 3, 4, 23, 3, null, null, "PUBV2SHARD", 3L, false, null);
        assertEquals(3, q.getMessageRefreshInterval());
        assertEquals(4, q.getUnackTime());
        assertEquals(23, q.getMessageTimeout());
        assertEquals("PUBV2SHARD", q.getUnAckShardName());
        assertFalse(q.isRequeueOnTimeout());
        assertEquals(3L, q.getRequeueCheckTimeoutMillis());
    }

    @Test
    public void testShardIdSetPublic() {
        RedisDynoQueue queue = new RedisDynoQueue(null, "queueV2Public", null, 12, 0, 101, 5, null, null, "shardV2Pub", 0L, false, null);
        assertEquals("shardV2Pub", queue.getUnAckShardName());
    }
}