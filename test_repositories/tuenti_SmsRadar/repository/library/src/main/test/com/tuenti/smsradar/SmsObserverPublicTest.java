package com.tuenti.smsradar;

import org.junit.Assert;
import org.junit.Test;

public class SmsObserverPublicTest {
    boolean trigger;

    @Test
    public void testOnSmsReceivedCallbackDiffData() {
        trigger = false;
        SmsListener listener = new SmsListener() {
            @Override
            public void onSmsReceived(Sms sms) {
                Assert.assertEquals("ObserverName", sms.getContact());
                Assert.assertEquals("+999999999", sms.getAddress());
                Assert.assertEquals("ObserverMsg", sms.getMessage());
                trigger = true;
            }
        };
        Sms sms = new Sms("ObserverName", "+999999999", "ObserverMsg", 1987654321L, SmsType.SENT);
        listener.onSmsReceived(sms);
        Assert.assertTrue(trigger);
    }
}