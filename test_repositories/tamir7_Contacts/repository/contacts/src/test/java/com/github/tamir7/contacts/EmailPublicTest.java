package com.github.tamir7.contacts;

import org.junit.Test;
import static org.junit.Assert.*;

public class EmailPublicTest {

    @Test
    public void testConstructorsAndGetters_Type() {
        Email e = new Email("test@public.com", Email.Type.HOME);
        assertEquals("test@public.com", e.getAddress());
        assertEquals(Email.Type.HOME, e.getType());
        assertNull(e.getLabel());
    }

    @Test
    public void testConstructorsAndGetters_Label() {
        Email e = new Email("alpha@beta.com", "office");
        assertEquals("alpha@beta.com", e.getAddress());
        assertEquals(Email.Type.CUSTOM, e.getType());
        assertEquals("office", e.getLabel());
    }

    @Test
    public void testEqualsAndHashCode() {
        Email e1 = new Email("unique@mail.com", Email.Type.MOBILE);
        Email e2 = new Email("unique@mail.com", Email.Type.MOBILE);
        Email e3 = new Email("unique@mail.com", "project");
        assertEquals(e1, e2);
        assertNotEquals(e1, e3);
        assertEquals(e1.hashCode(), e2.hashCode());
    }

    @Test
    public void testTypeFromValue() {
        assertEquals(Email.Type.CUSTOM, Email.Type.fromValue(-1)); // Custom is usually 0, try -1
        assertEquals(Email.Type.HOME, Email.Type.fromValue(1));
        assertEquals(Email.Type.WORK, Email.Type.fromValue(2));
        assertEquals(Email.Type.OTHER, Email.Type.fromValue(3));
        assertEquals(Email.Type.MOBILE, Email.Type.fromValue(4));
        assertEquals(Email.Type.UNKNOWN, Email.Type.fromValue(123));
    }

    @Test
    public void testNotEqualConditions() {
        Email e1 = new Email("nobody@nowhere.com", Email.Type.MOBILE);
        assertNotEquals(e1, null);
        assertNotEquals(e1, "NotAnEmailObject");
        Email e2 = new Email("someone@somewhere.com", Email.Type.MOBILE);
        assertNotEquals(e1, e2);
    }
}