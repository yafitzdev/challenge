package com.github.tamir7.contacts;

import org.junit.Test;
import static org.junit.Assert.*;

public class AddressPublicTest {

    @Test
    public void testConstructorsAndGetters_Type() {
        Address a = new Address("Street 123", "Townsville", "AA", "CountryX", "98765", Address.Type.WORK);
        assertEquals("Street 123", a.getStreet());
        assertEquals("Townsville", a.getCity());
        assertEquals("AA", a.getRegion());
        assertEquals("CountryX", a.getCountry());
        assertEquals("98765", a.getPostalCode());
        assertEquals(Address.Type.WORK, a.getType());
        assertNull(a.getLabel());
    }

    @Test
    public void testConstructorsAndGetters_Label() {
        Address a = new Address("Ave A", "Metropolis", "BB", "CountryY", "24680", "Vacation Spot");
        assertEquals("Ave A", a.getStreet());
        assertEquals("Metropolis", a.getCity());
        assertEquals("BB", a.getRegion());
        assertEquals("CountryY", a.getCountry());
        assertEquals("24680", a.getPostalCode());
        assertEquals(Address.Type.CUSTOM, a.getType());
        assertEquals("Vacation Spot", a.getLabel());
    }

    @Test
    public void testEqualsAndHashCode() {
        Address a1 = new Address("Zebra", "CityZ", "RR", "LandQ", "65432", Address.Type.HOME);
        Address a2 = new Address("Zebra", "CityZ", "RR", "LandQ", "65432", Address.Type.HOME);
        Address a3 = new Address("Zebra", "CityZ", "RR", "LandQ", "65432", "MyPlace");
        assertEquals(a1, a2);
        assertNotEquals(a1, a3);
        assertEquals(a1.hashCode(), a2.hashCode());
    }

    @Test
    public void testTypeFromValue() {
        assertEquals(Address.Type.CUSTOM, Address.Type.fromValue(-1));
        assertEquals(Address.Type.HOME, Address.Type.fromValue(1));
        assertEquals(Address.Type.WORK, Address.Type.fromValue(2));
        assertEquals(Address.Type.OTHER, Address.Type.fromValue(3));
        assertEquals(Address.Type.UNKNOWN, Address.Type.fromValue(100));
    }

    @Test
    public void testNotEqualConditions() {
        Address a1 = new Address("Alpha", "Beta", "Gamma", "Delta", "61616", Address.Type.WORK);
        assertNotEquals(a1, null);
        assertNotEquals(a1, "NotAnAddress");
        Address a2 = new Address("Beta", "Gamma", "Delta", "Epsilon", "89898", Address.Type.WORK);
        assertNotEquals(a1, a2);
    }
}