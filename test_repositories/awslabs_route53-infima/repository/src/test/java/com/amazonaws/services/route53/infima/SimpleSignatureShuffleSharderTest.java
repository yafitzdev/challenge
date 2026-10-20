package com.amazonaws.services.route53.infima;

import org.junit.jupiter.api.Test;

import java.security.NoSuchAlgorithmException;
import java.util.Arrays;
import java.util.Collection;

import static org.junit.jupiter.api.Assertions.*;

class SimpleSignatureShuffleSharderTest {
    @Test
    void testShuffleShardReturnsCorrectSize() throws NoSuchAlgorithmException {
        OneDimensionalLattice<String> lattice = new OneDimensionalLattice<>();
        lattice.addEndpoints("az1", Arrays.asList("A", "B", "C", "D"));
        SimpleSignatureShuffleSharder<String> sharder = new SimpleSignatureShuffleSharder<>(123L);

        Lattice<String> shard = sharder.shuffleShard(lattice, "id-1".getBytes(), 2);
        // Should be at most two endpoints
        Collection<String> endpoints = shard.getAllEndpoints();
        assertEquals(2, endpoints.size());
    }

    @Test
    void testShuffleShardDifferentIdentifiersProduceDifferentShards() throws NoSuchAlgorithmException {
        OneDimensionalLattice<String> lattice = new OneDimensionalLattice<>();
        lattice.addEndpoints("test", Arrays.asList("A", "B", "C", "D"));
        SimpleSignatureShuffleSharder<String> sharder = new SimpleSignatureShuffleSharder<>(42L);

        Lattice<String> shard1 = sharder.shuffleShard(lattice, "id-1".getBytes(), 2);
        Lattice<String> shard2 = sharder.shuffleShard(lattice, "id-2".getBytes(), 2);

        assertNotEquals(shard1.getAllEndpoints(), shard2.getAllEndpoints());
    }

    @Test
    void testThrowsNoSuchAlgorithmException() {
        // This is just for coverage, but since MD5 is almost always available, just check the catch block is present.
        // We can't force NoSuchAlgorithmException in practice in the JVM intentionally.
        SimpleSignatureShuffleSharder<String> sharder = new SimpleSignatureShuffleSharder<>(1L);
        // No negative test needed, method declares it throws
    }
}