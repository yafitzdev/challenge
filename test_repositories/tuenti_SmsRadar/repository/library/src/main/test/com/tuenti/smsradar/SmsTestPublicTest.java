package com.tuenti.smsradar;

import org.junit.Assert;
import org.junit.Test;

public class SmsTestPublicTest {

    @Test
    public void testConstructorAndGettersDifferentData() {
        Sms sms = new Sms("PublicTestContact", "+10987654321", "Hello Public Test!", 1440000000L, SmsType.DRAFT);
        Assert.assertEquals("PublicTestContact", sms.getContact());
        Assert.assertEquals("+10987654321", sms.getAddress());
        Assert.assertEquals("Hello Public Test!", sms.getMessage());
        Assert.assertEquals(1440000000L, sms.getTime());
        Assert.assertEquals(SmsType.DRAFT, sms.getType());
    }

    @Test
    public void testSmsEqualsDifferentData() {
        Sms sms1 = new Sms("AA", "BB", "CC", 55555555L, SmsType.OUTBOX);
        Sms sms2 = new Sms("AA", "BB", "CC", 55555555L, SmsType.OUTBOX);
        Assert.assertEquals(sms1, sms2);
    }

    @Test
    public void testSmsToStringDifferentData() {
        Sms sms = new Sms("XY", "ZZ", "MessageTest", 66778899L, SmsType.DRAFT);
        String str = sms.toString();
        Assert.assertTrue(str.contains("XY"));
        Assert.assertTrue(str.contains("ZZ"));
        Assert.assertTrue(str.contains("MessageTest"));
        Assert.assertTrue(str.contains("66778899"));
        Assert.assertTrue(str.contains("DRAFT"));
    }
}