package com.netflix.dyno.queues.redis;

import com.netflix.dyno.connectionpool.Host;
import com.netflix.dyno.connectionpool.HostSupplier;
import org.junit.Test;

import java.util.*;

import static org.junit.Assert.*;

public class DynoShardSupplierPublicTest {

    private static class DummyHostSupplier implements HostSupplier {
        private final List<Host> hosts;
        DummyHostSupplier(List<Host> hosts) { this.hosts = hosts; }
        @Override
        public List<Host> getHosts() { return hosts; }
    }

    @Test
    public void testGetQueueShards() {
        List<Host> hosts = Arrays.asList(
                new Host("pubhost1", 8100, "zonePub1", Host.Status.Up),
                new Host("pubhost2", 8100, "zonePub2", Host.Status.Up),
                new Host("pubhost3", 8100, "zonePub3", Host.Status.Up)
        );
        DynoShardSupplier supplier = new DynoShardSupplier(new DummyHostSupplier(hosts), "zonePub2");
        Set<String> shards = supplier.getQueueShards();
        assertTrue(shards.contains("zonePub1"));
        assertTrue(shards.contains("zonePub2"));
        assertTrue(shards.contains("zonePub3"));
    }

    @Test
    public void testCurrentShard() {
        List<Host> hosts = Arrays.asList(
                new Host("pubhostA", 9100, "regionX", Host.Status.Up)
        );
        DynoShardSupplier supplier = new DynoShardSupplier(new DummyHostSupplier(hosts), "regionX");
        assertEquals("regionX", supplier.getCurrentShard());
    }

    @Test
    public void testGetShardForHost() {
        Host host = new Host("pubhostB", 10000, "rrrack", Host.Status.Up);
        DynoShardSupplier supplier = new DynoShardSupplier(null, "");
        assertEquals("rrrack", supplier.getShardForHost(host));
    }
}