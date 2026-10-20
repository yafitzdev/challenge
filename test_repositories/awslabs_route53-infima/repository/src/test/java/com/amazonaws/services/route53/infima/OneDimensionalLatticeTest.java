package com.amazonaws.services.route53.infima;

import org.junit.jupiter.api.Test;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;

public class OneDimensionalLatticeTest {

    @Test
    public void testConstructorWithName() {
        OneDimensionalLattice<String> lattice = new OneDimensionalLattice<>("Zone");
        assertNotNull(lattice);
        assertEquals(Arrays.asList("Zone"), lattice.getDimensionNames());
    }

    @Test
    public void testDefaultConstructor() {
        OneDimensionalLattice<String> lattice = new OneDimensionalLattice<>();
        assertNotNull(lattice);
        assertEquals(Arrays.asList("AvailabilityZone"), lattice.getDimensionNames());
    }

    @Test
    public void testAddAndGetEndpoints() {
        OneDimensionalLattice<String> lattice = new OneDimensionalLattice<>();
        lattice.addEndpoints("us-east-1a", Arrays.asList("A", "B"));
        Collection<String> result = lattice.getEndpoints("us-east-1a");
        assertTrue(result.contains("A"));
        assertTrue(result.contains("B"));
    }

    @Test
    public void testAddEndpoint() {
        OneDimensionalLattice<String> lattice = new OneDimensionalLattice<>();
        lattice.addEndpoint("us-west-2", "Foo");
        Collection<String> res = lattice.getEndpoints("us-west-2");
        assertEquals(1, res.size());
        assertTrue(res.contains("Foo"));
    }

    @Test
    public void testEmptyEndpoints() {
        OneDimensionalLattice<String> lattice = new OneDimensionalLattice<>();
        assertTrue(lattice.getEndpoints("nonexistent").isEmpty());
    }
}