package com.netflix.dyno.queues.redis;

import com.netflix.dyno.queues.Message;
import com.netflix.dyno.queues.ShardSupplier;
import org.junit.Before;
import org.junit.Test;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

import static org.junit.Assert.*;

public class DefaultShardingStrategyPublicTest {

    private DefaultShardingStrategy strategy;

    @Before
    public void setUp() {
        strategy = new DefaultShardingStrategy();
    }

    @Test
    public void testGetShardLargeSet() {
        Set<String> shards = new HashSet<>();
        shards.add("red");
        shards.add("blue");
        ShardSupplier supplier = new ShardSupplier() {
            @Override
            public Set<String> getQueueShards() { return shards; }
            @Override
            public String getCurrentShard() { return "blue"; }
            @Override
            public String getShardForHost(com.netflix.dyno.connectionpool.Host host) { return "red"; }
        };

        Message msg = new Message("random", "someval");
        String shard = strategy.getShard(msg, supplier);
        assertNotNull(shard);
        assertTrue(shards.contains(shard));
    }

    @Test
    public void testGetShardEmptySet() {
        ShardSupplier supplier = new ShardSupplier() {
            @Override
            public Set<String> getQueueShards() { return Collections.emptySet(); }
            @Override
            public String getCurrentShard() { return null; }
            @Override
            public String getShardForHost(com.netflix.dyno.connectionpool.Host host) { return null; }
        };
        Message msg = new Message("m2", "v2");
        assertNull(strategy.getShard(msg, supplier));
    }
}