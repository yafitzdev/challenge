package com.tuenti.smsradar;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import java.util.List;

public class SmsStoragePublicTest {

    private SmsStorage smsStorage;

    @Before
    public void setUp() {
        smsStorage = new SmsStorage();
    }

    @Test
    public void testStoreAndGetSingleSms() {
        Sms sms = new Sms("Charlie", "+1987654321", "Hey there!", 1357924680L, SmsType.INBOX);
        smsStorage.storeSms(sms);
        List<Sms> retrieved = smsStorage.getAllSms();
        Assert.assertEquals(1, retrieved.size());
        Sms out = retrieved.get(0);
        Assert.assertEquals("Charlie", out.getContact());
        Assert.assertEquals("+1987654321", out.getAddress());
        Assert.assertEquals("Hey there!", out.getMessage());
    }

    @Test
    public void testStoreMultipleSms() {
        Sms s1 = new Sms("Delta", "+1234509876", "First msg", 1000000100L, SmsType.SENT);
        Sms s2 = new Sms("Echo", "+1987654322", "Second msg", 1000000200L, SmsType.OUTBOX);
        smsStorage.storeSms(s1);
        smsStorage.storeSms(s2);
        List<Sms> list = smsStorage.getAllSms();
        Assert.assertEquals(2, list.size());
        Assert.assertEquals("First msg", list.get(0).getMessage());
        Assert.assertEquals("Second msg", list.get(1).getMessage());
    }

    @Test
    public void testStorageIsCleared() {
        smsStorage.storeSms(new Sms("Foxtrot", "+1324354657", "To clear", 1234000000L, SmsType.DRAFT));
        smsStorage.clearAll();
        Assert.assertTrue(smsStorage.getAllSms().isEmpty());
    }
}