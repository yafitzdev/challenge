package com.amazonaws.services.route53.infima;

import org.junit.jupiter.api.Test;
import java.util.Arrays;
import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;

public class TwoDimensionalLatticeTest {

    @Test
    public void testConstructorAndDimensionNames() {
        TwoDimensionalLattice<String> lattice = new TwoDimensionalLattice<>("D1", "D2");
        assertEquals(Arrays.asList("D1", "D2"), lattice.getDimensionNames());
    }

    @Test
    public void testAddEndpointsAndGetEndpoints() {
        TwoDimensionalLattice<String> lattice = new TwoDimensionalLattice<>("X", "Y");
        lattice.addEndpoints("a", "b", Arrays.asList("foo", "bar"));
        assertTrue(lattice.getEndpoints("a", "b").containsAll(Arrays.asList("foo", "bar")));
    }

    @Test
    public void testAddEndpoint() {
        TwoDimensionalLattice<String> lattice = new TwoDimensionalLattice<>("A", "B");
        lattice.addEndpoint("X", "Y", "Z");
        assertEquals(Collections.singleton("Z"), lattice.getEndpoints("X", "Y"));
    }

    @Test
    public void testGetEndpointsNotPresent() {
        TwoDimensionalLattice<String> lattice = new TwoDimensionalLattice<>("DD1", "DD2");
        assertTrue(lattice.getEndpoints("no", "key").isEmpty());
    }
}