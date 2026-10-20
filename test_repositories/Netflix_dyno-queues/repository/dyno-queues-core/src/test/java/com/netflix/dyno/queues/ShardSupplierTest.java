package com.netflix.dyno.queues;

import org.junit.Test;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

import static org.junit.Assert.*;

public class ShardSupplierTest {

    private static class TestShardSupplier implements ShardSupplier {
        private Set<String> shards;
        private String currentShard;
        public TestShardSupplier(Set<String> shards, String currentShard) {
            this.shards = shards;
            this.currentShard = currentShard;
        }
        @Override
        public Set<String> getQueueShards() { return shards; }
        @Override
        public String getCurrentShard() { return currentShard; }
        @Override
        public String getShardForHost(com.netflix.dyno.connectionpool.Host host) {
            // return rack name for testing
            return host.getRack();
        }
    }

    @Test
    public void testShardSupplierInterface() {
        Set<String> shards = new HashSet<>();
        shards.add("one");
        shards.add("two");
        TestShardSupplier supplier = new TestShardSupplier(shards, "one");

        assertEquals(shards, supplier.getQueueShards());
        assertEquals("one", supplier.getCurrentShard());
        com.netflix.dyno.connectionpool.Host host = new com.netflix.dyno.connectionpool.Host("host", 1, "rck", com.netflix.dyno.connectionpool.Host.Status.Up);
        assertEquals("rck", supplier.getShardForHost(host));
    }

    @Test
    public void testShardSupplierEmptySet() {
        TestShardSupplier supplier = new TestShardSupplier(Collections.emptySet(), null);
        assertTrue(supplier.getQueueShards().isEmpty());
        assertNull(supplier.getCurrentShard());
    }
}