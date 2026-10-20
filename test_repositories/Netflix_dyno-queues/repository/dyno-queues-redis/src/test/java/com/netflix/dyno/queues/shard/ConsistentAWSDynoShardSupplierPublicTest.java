package com.netflix.dyno.queues.shard;

import com.netflix.dyno.connectionpool.Host;
import com.netflix.dyno.connectionpool.HostSupplier;
import org.junit.Before;
import org.junit.Test;

import java.util.*;

import static org.junit.Assert.*;

public class ConsistentAWSDynoShardSupplierPublicTest {

    private TestHostSupplier supplier;
    private ConsistentAWSDynoShardSupplier shardSupplier;

    private static class TestHostSupplier implements HostSupplier {
        private final List<Host> hosts;
        public TestHostSupplier(List<Host> hosts) { this.hosts = hosts; }
        @Override
        public List<Host> getHosts() { return hosts; }
    }

    @Before
    public void setUp() {
        List<Host> hosts = Arrays.asList(
                new Host("serverA", 4567, "us-west-2a", Host.Status.Up),
                new Host("serverB", 4567, "us-west-2b", Host.Status.Up),
                new Host("serverC", 4567, "us-west-2c", Host.Status.Up),
                new Host("serverD", 4567, "eu-west-1a", Host.Status.Up)
        );
        supplier = new TestHostSupplier(hosts);
        shardSupplier = new ConsistentAWSDynoShardSupplier(supplier, "us-west-2", "us-west-2b");
    }

    @Test
    public void testGetCurrentShard() {
        assertEquals("b", shardSupplier.getCurrentShard());
        ConsistentAWSDynoShardSupplier s2 = new ConsistentAWSDynoShardSupplier(supplier, "us-west-2", "us-west-2c");
        assertEquals("c", s2.getCurrentShard());
        ConsistentAWSDynoShardSupplier s3 = new ConsistentAWSDynoShardSupplier(supplier, "us-west-2", "nonexistent");
        assertNull(s3.getCurrentShard());
    }

    @Test
    public void testGetQueueShards() {
        Set<String> shards = shardSupplier.getQueueShards();
        // Should include new canonical values (a, b, c)
        assertTrue(shards.contains("a"));
        assertTrue(shards.contains("b"));
        assertTrue(shards.contains("c"));
        assertTrue(shards.size() <= 4);
    }

    @Test
    public void testGetShardForHost() {
        Host hostA = new Host("serverA", 4567, "us-west-2a", Host.Status.Up);
        Host hostB = new Host("serverD", 4567, "eu-west-1b", Host.Status.Up);
        Host hostUnknown = new Host("serverUnknown", 4567, "mystery", Host.Status.Up);

        assertEquals("a", shardSupplier.getShardForHost(hostA));
        assertEquals("b", shardSupplier.getShardForHost(hostB));
        assertNull(shardSupplier.getShardForHost(hostUnknown));
    }
}