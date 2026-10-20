package com.netflix.dyno.queues;

import org.junit.Test;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

import static org.junit.Assert.*;

public class ShardSupplierPublicTest {

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
            // return host's hostname for testing public case
            return host.getHostName();
        }
    }

    @Test
    public void testShardSupplierInterface() {
        Set<String> shards = new HashSet<>();
        shards.add("alpha");
        shards.add("beta");
        TestShardSupplier supplier = new TestShardSupplier(shards, "beta");

        assertEquals(shards, supplier.getQueueShards());
        assertEquals("beta", supplier.getCurrentShard());
        com.netflix.dyno.connectionpool.Host host = new com.netflix.dyno.connectionpool.Host("hostY", 2, "rackX", com.netflix.dyno.connectionpool.Host.Status.Up);
        assertEquals("hostY", supplier.getShardForHost(host));
    }

    @Test
    public void testShardSupplierEmptySet() {
        TestShardSupplier supplier = new TestShardSupplier(Collections.emptySet(), null);
        assertTrue(supplier.getQueueShards().isEmpty());
        assertNull(supplier.getCurrentShard());
    }
}