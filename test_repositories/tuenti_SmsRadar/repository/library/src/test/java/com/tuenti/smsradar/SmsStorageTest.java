package com.tuenti.smsradar;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.List;

public class SmsStorageTest {

    @Test
    public void testAddAndGetAllSms() {
        SmsStorage storage = new SmsStorage();
        Sms sms1 = new Sms("1", "111", "msg1", SmsType.RECEIVED);
        Sms sms2 = new Sms("2", "222", "msg2", SmsType.SENT);
        storage.addSms(sms1);
        storage.addSms(sms2);

        List<Sms> all = storage.getAllSms();
        assertEquals(2, all.size());
        assertTrue(all.contains(sms1));
        assertTrue(all.contains(sms2));
    }

    @Test
    public void testClear() {
        SmsStorage storage = new SmsStorage();
        storage.addSms(new Sms("1", "111", "msg1", SmsType.RECEIVED));
        storage.clear();
        assertTrue(storage.getAllSms().isEmpty());
    }
}