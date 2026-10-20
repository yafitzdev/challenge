package com.tuenti.smsradar;

import org.junit.Test;
import static org.junit.Assert.*;

public class SmsTypeTest {
    @Test
    public void testSmsTypeValues() {
        assertEquals(-1, SmsType.UNKNOWN.getValue());
        assertEquals(1, SmsType.RECEIVED.getValue());
        assertEquals(2, SmsType.SENT.getValue());
    }

    @Test
    public void testValueOf() {
        assertEquals(SmsType.UNKNOWN, SmsType.valueOf("UNKNOWN"));
        assertEquals(SmsType.RECEIVED, SmsType.valueOf("RECEIVED"));
        assertEquals(SmsType.SENT, SmsType.valueOf("SENT"));
    }
}