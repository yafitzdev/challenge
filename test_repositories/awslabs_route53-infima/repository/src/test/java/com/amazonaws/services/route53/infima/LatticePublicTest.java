package com.amazonaws.services.route53.infima;

import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class LatticePublicTest {

    @Test
    void testConstructionAndDimensionNamesWithDifferentDims() {
        List<String> dims = Arrays.asList("dimA", "dimB");
        Lattice<Integer> lattice = new Lattice<>(dims);
        assertEquals(dims, lattice.getDimensionNames());
    }

    @Test
    void testAddEndpointsForSectorAndGetEndpointsDifferent() {
        Lattice<String> lattice = new Lattice<>(Collections.singletonList("y"));
        List<String> coord = Collections.singletonList("custom");
        lattice.addEndpointsForSector(coord, Arrays.asList("P", "Q"));
        assertTrue(lattice.getEndpointsForSector(coord).contains("P"));
        assertTrue(lattice.getEndpointsForSector(coord).contains("Q"));
    }

    @Test
    void testSimulateFailureDifferentValues() {
        Lattice<String> lattice = new Lattice<>(Arrays.asList("country", "city"));
        List<String> coord1 = Arrays.asList("Spain", "Madrid");
        lattice.addEndpointsForSector(coord1, Arrays.asList("Server1", "Server2"));

        Lattice<String> failed = lattice.simulateFailure("country", "Spain");
        assertTrue(failed.getAllEndpoints().isEmpty() || failed.getEndpointsForSector(Arrays.asList("Spain", "Madrid")).isEmpty());
    }

    @Test
    void testGetDimensionValuesAndDimensionalityPublic() {
        Lattice<String> lattice = new Lattice<>(Arrays.asList("continent", "region"));
        lattice.addEndpointsForSector(Arrays.asList("Europe", "North"), Arrays.asList("HostA"));
        lattice.addEndpointsForSector(Arrays.asList("Europe", "South"), Arrays.asList("HostB"));
        Set<String> regions = new HashSet<>(lattice.getDimensionValues("region"));
        assertTrue(regions.contains("North"));
        assertTrue(regions.contains("South"));
        Map<String, Integer> dims = lattice.getDimensionality();
        assertEquals(2, dims.size());
    }

    @Test
    void testEqualsAndHashCodeDifferentData() {
        Lattice<String> l1 = new Lattice<>(Arrays.asList("R", "S"));
        Lattice<String> l2 = new Lattice<>(Arrays.asList("R", "S"));
        l1.addEndpointsForSector(Arrays.asList("foo", "bar"), Arrays.asList("baz"));
        l2.addEndpointsForSector(Arrays.asList("foo", "bar"), Arrays.asList("baz"));
        assertEquals(l1, l2);
        assertEquals(l1.hashCode(), l2.hashCode());
    }

    @Test
    void testToStringNotNullPublic() {
        Lattice<String> lattice = new Lattice<>(Collections.singletonList("E"));
        assertNotNull(lattice.toString());
    }

    @Test
    void testNoEndpointsPublic() {
        Lattice<String> lattice = new Lattice<>(Collections.singletonList("F"));
        assertTrue(lattice.getAllEndpoints().isEmpty());
    }
}