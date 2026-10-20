package com.tuenti.smsradar;

import org.junit.Test;
import static org.junit.Assert.*;

public class SmsTest {

    @Test
    public void testConstructorAndGetters() {
        Sms sms = new Sms("12345", "1687221000000", "Hello there!", SmsType.RECEIVED);
        assertEquals("12345", sms.getAddress());
        assertEquals("1687221000000", sms.getDate());
        assertEquals("Hello there!", sms.getMsg());
        assertEquals(SmsType.RECEIVED, sms.getType());
    }

    @Test
    public void testEqualsHashCodeAndToString() {
        Sms a = new Sms("a", "111", "body", SmsType.RECEIVED);
        Sms b = new Sms("a", "111", "body", SmsType.RECEIVED);
        Sms c = new Sms("b", "112", "other", SmsType.SENT);

        assertEquals(a, b);
        assertEquals(a.hashCode(), b.hashCode());
        assertNotEquals(a, c);
        assertNotEquals(a.hashCode(), c.hashCode());
        assertTrue(a.toString().contains("body"));
    }

    @Test
    public void testNotEqualWithNullOrOtherType() {
        Sms sms = new Sms("a", "c", "b", SmsType.UNKNOWN);
        assertNotEquals(null, sms);
        assertNotEquals("Some String", sms);
    }
}