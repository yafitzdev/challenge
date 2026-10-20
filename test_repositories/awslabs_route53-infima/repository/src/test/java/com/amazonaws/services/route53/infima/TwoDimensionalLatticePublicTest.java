package com.amazonaws.services.route53.infima;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Arrays;
import java.util.Collection;

public class TwoDimensionalLatticePublicTest {
    @Test
    public void testAddAndGetEndpointsDifferentData() {
        TwoDimensionalLattice<String> lattice = new TwoDimensionalLattice<>("rack", "slot");
        lattice.addEndpoints("rack-17", "slot-9", Arrays.asList("R", "S", "T"));
        Collection<String> found = lattice.getEndpoints("rack-17", "slot-9");
        assertTrue(found.contains("R"));
        assertTrue(found.contains("S"));
        assertTrue(found.contains("T"));
    }

    @Test
    public void testAddEndpointDifferentData() {
        TwoDimensionalLattice<String> lattice = new TwoDimensionalLattice<>("zoneA", "rowB");
        lattice.addEndpoint("foo", "bar", "X");
        Collection<String> found = lattice.getEndpoints("foo", "bar");
        assertTrue(found.contains("X"));
        assertEquals(1, found.size());
    }

    @Test
    public void testGetEndpointsForNonexistentCoordinatesPublic() {
        TwoDimensionalLattice<String> lattice = new TwoDimensionalLattice<>("c", "d");
        assertTrue(lattice.getEndpoints("doesnot", "exist").isEmpty());
    }

    @Test
    public void testDimensionNamesPublic() {
        TwoDimensionalLattice<String> lattice = new TwoDimensionalLattice<>("fruit", "color");
        assertEquals(Arrays.asList("fruit", "color"), lattice.getDimensionNames());
    }
}