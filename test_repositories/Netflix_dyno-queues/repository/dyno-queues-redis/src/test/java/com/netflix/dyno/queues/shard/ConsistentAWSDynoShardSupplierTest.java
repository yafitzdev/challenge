package com.netflix.dyno.queues.shard;

import com.netflix.dyno.connectionpool.Host;
import com.netflix.dyno.connectionpool.HostSupplier;
import org.junit.Before;
import org.junit.Test;

import java.util.*;

import static org.junit.Assert.*;

public class ConsistentAWSDynoShardSupplierTest {

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
                new Host("host1", 1234, "us-east-1c", Host.Status.Up),
                new Host("host2", 1234, "us-east-1d", Host.Status.Up),
                new Host("host3", 1234, "us-east-1e", Host.Status.Up),
                new Host("host4", 1234, "us-west-2a", Host.Status.Up)
        );
        supplier = new TestHostSupplier(hosts);
        shardSupplier = new ConsistentAWSDynoShardSupplier(supplier, "us-east-1", "us-east-1c");
    }

    @Test
    public void testGetCurrentShard() {
        assertEquals("c", shardSupplier.getCurrentShard());
        ConsistentAWSDynoShardSupplier s2 = new ConsistentAWSDynoShardSupplier(supplier, "us-east-1", "us-east-1d");
        assertEquals("d", s2.getCurrentShard());
        ConsistentAWSDynoShardSupplier s3 = new ConsistentAWSDynoShardSupplier(supplier, "us-east-1", "foo");
        assertNull(s3.getCurrentShard());
    }

    @Test
    public void testGetQueueShards() {
        Set<String> shards = shardSupplier.getQueueShards();
        // Should be only the canonical values (c, d, e)
        assertTrue(shards.contains("c"));
        assertTrue(shards.contains("d"));
        assertTrue(shards.contains("e"));
        // us-west-2a also maps to "c", so size <= hosts
        assertTrue(shards.size() <= 4);
    }

    @Test
    public void testGetShardForHost() {
        Host hostA = new Host("host1", 1234, "us-east-1c", Host.Status.Up);
        Host hostB = new Host("host2", 1234, "us-west-2b", Host.Status.Up);
        Host hostUnknown = new Host("hostX", 1234, "unknown", Host.Status.Up);

        assertEquals("c", shardSupplier.getShardForHost(hostA));
        assertEquals("d", shardSupplier.getShardForHost(hostB));
        assertNull(shardSupplier.getShardForHost(hostUnknown));
    }
}