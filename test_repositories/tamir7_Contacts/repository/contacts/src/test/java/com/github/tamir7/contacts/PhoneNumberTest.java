package com.github.tamir7.contacts;

import org.junit.Test;
import static org.junit.Assert.*;

public class PhoneNumberTest {

    @Test
    public void testConstructorsAndGetters_Type() {
        PhoneNumber p = new PhoneNumber("12345", PhoneNumber.Type.HOME, "54321");
        assertEquals("12345", p.getNumber());
        assertEquals("54321", p.getNormalizedNumber());
        assertEquals(PhoneNumber.Type.HOME, p.getType());
        assertNull(p.getLabel());
    }

    @Test
    public void testConstructorsAndGetters_Label() {
        PhoneNumber p = new PhoneNumber("333", "mobile label", "333");
        assertEquals("333", p.getNumber());
        assertEquals("mobile label", p.getLabel());
        assertEquals(PhoneNumber.Type.CUSTOM, p.getType());
        assertEquals("333", p.getNormalizedNumber());
    }

    @Test
    public void testEqualsAndHashCode() {
        PhoneNumber p1 = new PhoneNumber("123", PhoneNumber.Type.HOME, "abc");
        PhoneNumber p2 = new PhoneNumber("123", PhoneNumber.Type.HOME, "abc");
        PhoneNumber p3 = new PhoneNumber("999", PhoneNumber.Type.HOME, "abc");
        assertEquals(p1, p2);
        assertNotEquals(p1, p3);
        assertEquals(p1.hashCode(), p2.hashCode());
    }

    @Test
    public void testTypeFromValue() {
        assertEquals(PhoneNumber.Type.CUSTOM, PhoneNumber.Type.fromValue(0));
        assertEquals(PhoneNumber.Type.HOME, PhoneNumber.Type.fromValue(1));
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
        assertEquals(PhoneNumber.Type.UNKNOWN, PhoneNumber.Type.fromValue(999));
    }

    @Test
    public void testNotEqualConditions() {
        PhoneNumber p1 = new PhoneNumber("x", PhoneNumber.Type.HOME, "n");
        assertNotEquals(p1, null);
        assertNotEquals(p1, "notPhone");
        PhoneNumber p2 = new PhoneNumber("different", PhoneNumber.Type.HOME, "n");
        assertNotEquals(p1, p2);
    }
}