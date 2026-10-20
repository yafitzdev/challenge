package com.tuenti.smsradar;

import org.junit.Test;

import java.util.Date;

import static org.junit.Assert.*;

public class TimeProviderTest {

    @Test
    public void testGetDateReturnsNow() {
        TimeProvider provider = new TimeProvider();
        Date before = new Date();
        Date result = provider.getDate();
        Date after = new Date();

        assertNotNull(result);
        assertTrue(result.getTime() >= before.getTime() && result.getTime() <= after.getTime());
    }
}