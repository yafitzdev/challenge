package com.amazonaws.services.route53.infima;

import org.junit.jupiter.api.Test;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;

public class OneDimensionalLatticePublicTest {

    @Test
    public void testConstructorWithNameDifferent() {
        OneDimensionalLattice<String> lattice = new OneDimensionalLattice<>("ZoneX");
        assertNotNull(lattice);
        assertEquals(Arrays.asList("ZoneX"), lattice.getDimensionNames());
    }

    @Test
    public void testDefaultConstructorPublic() {
        OneDimensionalLattice<String> lattice = new OneDimensionalLattice<>();
        assertNotNull(lattice);
        assertEquals(Arrays.asList("AvailabilityZone"), lattice.getDimensionNames());
    }

    @Test
    public void testAddAndGetEndpointsDifferentData() {
        OneDimensionalLattice<String> lattice = new OneDimensionalLattice<>();
        lattice.addEndpoints("eu-central-1b", Arrays.asList("M", "N"));
        Collection<String> result = lattice.getEndpoints("eu-central-1b");
        assertTrue(result.contains("M"));
        assertTrue(result.contains("N"));
    }

    @Test
    public void testAddEndpointDifferentData() {
        OneDimensionalLattice<String> lattice = new OneDimensionalLattice<>();
        lattice.addEndpoint("eu-north-1", "Bar");
        Collection<String> res = lattice.getEndpoints("eu-north-1");
        assertEquals(1, res.size());
        assertTrue(res.contains("Bar"));
    }

    @Test
    public void testEmptyEndpointsPublic() {
        OneDimensionalLattice<String> lattice = new OneDimensionalLattice<>();
        assertTrue(lattice.getEndpoints("doesnotexist").isEmpty());
    }
}