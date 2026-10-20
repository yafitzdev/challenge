package com.netflix.dyno.queues.redis;

import com.netflix.dyno.queues.Message;
import com.netflix.dyno.queues.ShardSupplier;
import org.junit.Test;

import java.util.Collections;

import static org.junit.Assert.*;

public class CustomShardingStrategyPublicTest {

    @Test
    public void testGetShardWithPayload() {
        ShardSupplier supplier = new ShardSupplier() {
            @Override
            public java.util.Set<String> getQueueShards() {
                java.util.Set<String> set = new java.util.HashSet<>();
                set.add("foo");
                set.add("bar");
                return set;
            }
            @Override
            public String getCurrentShard() { return "foo"; }
            @Override
            public String getShardForHost(com.netflix.dyno.connectionpool.Host host) { return "bar"; }
        };
        Message msg = new Message("pubid", "payload_custom");
        CustomShardingStrategy strategy = new CustomShardingStrategy();
        String shard = strategy.getShard(msg, supplier);
        assertTrue(shard.equals("foo") || shard.equals("bar"));
    }

    @Test
    public void testGetShardReturnsNullWithEmptySet() {
        ShardSupplier supplier = new ShardSupplier() {
            @Override
            public java.util.Set<String> getQueueShards() {
                return Collections.emptySet();
            }
            @Override
            public String getCurrentShard() { return null; }
            @Override
            public String getShardForHost(com.netflix.dyno.connectionpool.Host host) { return null; }
        };
        Message msg = new Message("pubid2", "payload_custom2");
        CustomShardingStrategy strategy = new CustomShardingStrategy();
        assertNull(strategy.getShard(msg, supplier));
    }
}