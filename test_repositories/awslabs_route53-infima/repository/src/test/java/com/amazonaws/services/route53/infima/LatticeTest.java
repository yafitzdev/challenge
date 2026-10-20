package com.amazonaws.services.route53.infima;

import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class LatticeTest {

    @Test
    void testConstructionAndDimensionNames() {
        List<String> dims = Arrays.asList("x", "y");
        Lattice<Integer> lattice = new Lattice<>(dims);
        assertEquals(dims, lattice.getDimensionNames());
    }

    @Test
    void testAddEndpointsForSectorAndGetEndpoints() {
        Lattice<String> lattice = new Lattice<>(Collections.singletonList("x"));
        List<String> coord = Collections.singletonList("test");
        lattice.addEndpointsForSector(coord, Arrays.asList("A", "B"));
        assertTrue(lattice.getEndpointsForSector(coord).contains("A"));
        assertTrue(lattice.getEndpointsForSector(coord).contains("B"));
    }

    @Test
    void testSimulateFailure() {
        Lattice<String> lattice = new Lattice<>(Arrays.asList("X", "Y"));
        List<String> coord1 = Arrays.asList("A", "B");
        lattice.addEndpointsForSector(coord1, Arrays.asList("E1", "E2"));

        Lattice<String> failed = lattice.simulateFailure("X", "A");
        // Should remove coordinates where X == "A"
        assertTrue(failed.getAllEndpoints().isEmpty() || failed.getEndpointsForSector(Arrays.asList("A", "B")).isEmpty());
    }

    @Test
    void testGetDimensionValuesAndDimensionality() {
        Lattice<String> lattice = new Lattice<>(Arrays.asList("X", "Y"));
        lattice.addEndpointsForSector(Arrays.asList("A", "B"), Arrays.asList("Z"));
        lattice.addEndpointsForSector(Arrays.asList("A", "C"), Arrays.asList("Q"));
        Set<String> yvals = new HashSet<>(lattice.getDimensionValues("Y"));
        assertTrue(yvals.contains("B"));
        assertTrue(yvals.contains("C"));
        Map<String, Integer> dims = lattice.getDimensionality();
        assertEquals(2, dims.size());
    }

    @Test
    void testEqualsAndHashCode() {
        Lattice<String> l1 = new Lattice<>(Arrays.asList("X", "Y"));
        Lattice<String> l2 = new Lattice<>(Arrays.asList("X", "Y"));
        l1.addEndpointsForSector(Arrays.asList("A", "B"), Arrays.asList("Q"));
        l2.addEndpointsForSector(Arrays.asList("A", "B"), Arrays.asList("Q"));
        assertEquals(l1, l2);
        assertEquals(l1.hashCode(), l2.hashCode());
    }

    @Test
    void testToStringNotNull() {
        Lattice<String> lattice = new Lattice<>(Collections.singletonList("D"));
        assertNotNull(lattice.toString());
    }

    @Test
    void testNoEndpoints() {
        Lattice<String> lattice = new Lattice<>(Collections.singletonList("D"));
        assertTrue(lattice.getAllEndpoints().isEmpty());
    }
}