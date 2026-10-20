package com.github.tamir7.contacts;

import org.junit.Test;
import static org.junit.Assert.*;

public class EmailTest {

    @Test
    public void testConstructorsAndGetters_Type() {
        Email e = new Email("addr@email.com", Email.Type.WORK);
        assertEquals("addr@email.com", e.getAddress());
        assertEquals(Email.Type.WORK, e.getType());
        assertNull(e.getLabel());
    }

    @Test
    public void testConstructorsAndGetters_Label() {
        Email e = new Email("foo@bar.com", "mylabel");
        assertEquals("foo@bar.com", e.getAddress());
        assertEquals(Email.Type.CUSTOM, e.getType());
        assertEquals("mylabel", e.getLabel());
    }

    @Test
    public void testEqualsAndHashCode() {
        Email e1 = new Email("x@x.com", Email.Type.HOME);
        Email e2 = new Email("x@x.com", Email.Type.HOME);
        Email e3 = new Email("x@x.com", "label");
        assertEquals(e1, e2);
        assertNotEquals(e1, e3);
        assertEquals(e1.hashCode(), e2.hashCode());
    }

    @Test
    public void testTypeFromValue() {
        assertEquals(Email.Type.CUSTOM, Email.Type.fromValue(0));
        assertEquals(Email.Type.HOME, Email.Type.fromValue(1));
        assertEquals(Email.Type.WORK, Email.Type.fromValue(2));
        assertEquals(Email.Type.OTHER, Email.Type.fromValue(3));
        assertEquals(Email.Type.MOBILE, Email.Type.fromValue(4));
        assertEquals(Email.Type.UNKNOWN, Email.Type.fromValue(99));
    }

    @Test
    public void testNotEqualConditions() {
        Email e1 = new Email("x@x.com", Email.Type.HOME);
        assertNotEquals(e1, null);
        assertNotEquals(e1, "notAnEmail");
        Email e2 = new Email("z@z.com", Email.Type.HOME);
        assertNotEquals(e1, e2);
    }
}