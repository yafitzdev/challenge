package com.github.tamir7.contacts;

import org.junit.Test;
import static org.junit.Assert.*;

public class AddressTest {

    @Test
    public void testGettersAndConstructors_Type() {
        Address a = new Address("addr", "str", "city", "reg", "zip", "country", Address.Type.HOME);
        assertEquals("addr", a.getFormattedAddress());
        assertEquals("str", a.getStreet());
        assertEquals("city", a.getCity());
        assertEquals("reg", a.getRegion());
        assertEquals("zip", a.getPostcode());
        assertEquals("country", a.getCountry());
        assertNull(a.getLabel());
        assertEquals(Address.Type.HOME, a.getType());
    }

    @Test
    public void testGettersAndConstructors_Label() {
        Address a = new Address("addr", "str", "city", "reg", "zip", "country", "myLabel");
        assertEquals("myLabel", a.getLabel());
        assertEquals(Address.Type.CUSTOM, a.getType());
    }

    @Test
    public void testTypeFromValue() {
        // Make up android constant values that correspond to the enum switches
        assertEquals(Address.Type.CUSTOM, Address.Type.fromValue(0)); // TYPE_CUSTOM
        assertEquals(Address.Type.HOME, Address.Type.fromValue(1));   // TYPE_HOME
        assertEquals(Address.Type.WORK, Address.Type.fromValue(2));   // TYPE_WORK
        assertEquals(Address.Type.OTHER, Address.Type.fromValue(3));  // TYPE_OTHER
        assertEquals(Address.Type.UNKNOWN, Address.Type.fromValue(99)); // Not mapped
    }
}