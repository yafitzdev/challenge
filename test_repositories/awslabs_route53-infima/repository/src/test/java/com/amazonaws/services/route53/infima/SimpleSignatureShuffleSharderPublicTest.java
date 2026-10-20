package com.amazonaws.services.route53.infima;

import org.junit.jupiter.api.Test;

import java.security.NoSuchAlgorithmException;
import java.util.Arrays;
import java.util.Collection;

import static org.junit.jupiter.api.Assertions.*;

class SimpleSignatureShuffleSharderPublicTest {
    @Test
    void testShuffleShardReturnsCorrectSizeWithDifferentData() throws NoSuchAlgorithmException {
        OneDimensionalLattice<String> lattice = new OneDimensionalLattice<>();
        lattice.addEndpoints("az2", Arrays.asList("W", "X", "Y", "Z"));
        SimpleSignatureShuffleSharder<String> sharder = new SimpleSignatureShuffleSharder<>(456L);

        Lattice<String> shard = sharder.shuffleShard(lattice, "unique-777".getBytes(), 3);
        // Should be at most three endpoints
        Collection<String> endpoints = shard.getAllEndpoints();
        assertEquals(3, endpoints.size());
    }

    @Test
    void testShuffleShardDifferentIdentifiersProduceDifferentShardsWithDifferentData() throws NoSuchAlgorithmException {
        OneDimensionalLattice<String> lattice = new OneDimensionalLattice<>();
        lattice.addEndpoints("public", Arrays.asList("X", "Y", "Z", "W"));
        SimpleSignatureShuffleSharder<String> sharder = new SimpleSignatureShuffleSharder<>(99L);

        Lattice<String> shard1 = sharder.shuffleShard(lattice, "alpha".getBytes(), 2);
        Lattice<String> shard2 = sharder.shuffleShard(lattice, "beta".getBytes(), 2);

        assertNotEquals(shard1.getAllEndpoints(), shard2.getAllEndpoints());
    }

    @Test
    void testThrowsNoSuchAlgorithmExceptionCoverageOnly() {
        // Coverage only, see comment in reference test
        SimpleSignatureShuffleSharder<String> sharder = new SimpleSignatureShuffleSharder<>(13L);
        // Nothing to test, but test kept for completeness
    }
}