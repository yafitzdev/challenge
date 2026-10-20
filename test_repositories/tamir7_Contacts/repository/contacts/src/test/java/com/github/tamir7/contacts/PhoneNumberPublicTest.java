package com.github.tamir7.contacts;

import org.junit.Test;
import static org.junit.Assert.*;

public class PhoneNumberPublicTest {

    @Test
    public void testConstructorsAndGetters_Type() {
        PhoneNumber p = new PhoneNumber("7770011", PhoneNumber.Type.MOBILE, "007770011");
        assertEquals("7770011", p.getNumber());
        assertEquals("007770011", p.getNormalizedNumber());
        assertEquals(PhoneNumber.Type.MOBILE, p.getType());
        assertNull(p.getLabel());
    }

    @Test
    public void testConstructorsAndGetters_Label() {
        PhoneNumber p = new PhoneNumber("20202", "office label", "20202");
        assertEquals("20202", p.getNumber());
        assertEquals("office label", p.getLabel());
        assertEquals(PhoneNumber.Type.CUSTOM, p.getType());
        assertEquals("20202", p.getNormalizedNumber());
    }

    @Test
    public void testEqualsAndHashCode() {
        PhoneNumber p1 = new PhoneNumber("3333", PhoneNumber.Type.WORK, "xyz");
        PhoneNumber p2 = new PhoneNumber("3333", PhoneNumber.Type.WORK, "xyz");
        PhoneNumber p3 = new PhoneNumber("1234", PhoneNumber.Type.WORK, "xyz");
        assertEquals(p1, p2);
        assertNotEquals(p1, p3);
        assertEquals(p1.hashCode(), p2.hashCode());
    }

    @Test
    public void testTypeFromValue() {
        assertEquals(PhoneNumber.Type.CUSTOM, PhoneNumber.Type.fromValue(-1));
        assertEquals(PhoneNumber.Type.MOBILE, PhoneNumber.Type.fromValue(2));
        assertEquals(PhoneNumber.Type.WORK, PhoneNumber.Type.fromValue(3));
        assertEquals(PhoneNumber.Type.FAX_WORK, PhoneNumber.Type.fromValue(4));
        assertEquals(PhoneNumber.Type.FAX_HOME, PhoneNumber.Type.fromValue(5));
        assertEquals(PhoneNumber.Type.PAGER, PhoneNumber.Type.fromValue(6));
        assertEquals(PhoneNumber.Type.OTHER, PhoneNumber.Type.fromValue(7));
        assertEquals(PhoneNumber.Type.CALLBACK, PhoneNumber.Type.fromValue(8));
        assertEquals(PhoneNumber.Type.CAR, PhoneNumber.Type.fromValue(9));
        assertEquals(PhoneNumber.Type.COMPANY_MAIN, PhoneNumber.Type.fromValue(10));
        assertEquals(PhoneNumber.Type.ISDN, PhoneNumber.Type.fromValue(11));
        assertEquals(PhoneNumber.Type.MAIN, PhoneNumber.Type.fromValue(12));
        assertEquals(PhoneNumber.Type.OTHER_FAX, PhoneNumber.Type.fromValue(13));
        assertEquals(PhoneNumber.Type.RADIO, PhoneNumber.Type.fromValue(14));
        assertEquals(PhoneNumber.Type.TELEX, PhoneNumber.Type.fromValue(15));
        assertEquals(PhoneNumber.Type.TTY_TDD, PhoneNumber.Type.fromValue(16));
        assertEquals(PhoneNumber.Type.WORK_MOBILE, PhoneNumber.Type.fromValue(17));
        assertEquals(PhoneNumber.Type.WORK_PAGER, PhoneNumber.Type.fromValue(18));
        assertEquals(PhoneNumber.Type.ASSISTANT, PhoneNumber.Type.fromValue(19));
        assertEquals(PhoneNumber.Type.MMS, PhoneNumber.Type.fromValue(20));
        assertEquals(PhoneNumber.Type.UNKNOWN, PhoneNumber.Type.fromValue(-999));
    }

    @Test
    public void testNotEqualConditions() {
        PhoneNumber p1 = new PhoneNumber("abc", PhoneNumber.Type.MOBILE, "num");
        assertNotEquals(p1, null);
        assertNotEquals(p1, 42);
        PhoneNumber p2 = new PhoneNumber("xyz", PhoneNumber.Type.MOBILE, "num");
        assertNotEquals(p1, p2);
    }
}