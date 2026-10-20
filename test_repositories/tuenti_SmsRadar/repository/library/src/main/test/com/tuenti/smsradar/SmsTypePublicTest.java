package com.tuenti.smsradar;

import org.junit.Assert;
import org.junit.Test;

public class SmsTypePublicTest {

    @Test
    public void testValueOf() {
        SmsType type = SmsType.valueOf("INBOX");
        Assert.assertEquals(SmsType.INBOX, type);

        type = SmsType.valueOf("SENT");
        Assert.assertEquals(SmsType.SENT, type);
    }

    @Test
    public void testOrdinalDifferentFromTest() {
        Assert.assertNotEquals("SENT".hashCode(), SmsType.OUTBOX.ordinal());
    }

    @Test
    public void testValuesArrayLength() {
        SmsType[] values = SmsType.values();
        Assert.assertTrue(values.length > 1);
    }
}