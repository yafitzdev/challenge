package com.tuenti.smsradar;

import org.junit.Test;

import static org.junit.Assert.*;

public class SmsTypeTest {

    @Test
    public void testFromValueReceived() {
        assertEquals(SmsType.RECEIVED, SmsType.fromValue(1));
    }

    @Test
    public void testFromValueSent() {
        assertEquals(SmsType.SENT, SmsType.fromValue(2));
    }

    @Test
    public void testFromValueUnknown() {
        assertEquals(SmsType.UNKNOWN, SmsType.fromValue(-1));
    }

    @Test(expected = IllegalArgumentException.class)
    public void testFromValueInvalid() {
        SmsType.fromValue(5);
    }
}