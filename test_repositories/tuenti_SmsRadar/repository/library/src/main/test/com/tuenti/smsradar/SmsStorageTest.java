package com.tuenti.smsradar;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class SmsStorageTest {

    private DummySmsStorage storage;

    @Before
    public void setUp() {
        storage = new DummySmsStorage();
    }

    @Test
    public void testIsFirstSmsInterceptedInitiallyTrue() {
        assertTrue(storage.isFirstSmsIntercepted());
    }

    @Test
    public void testUpdateAndGetLastSms() {
        storage.updateLastSmsIntercepted(42);
        assertFalse(storage.isFirstSmsIntercepted());
        assertEquals(42, storage.getLastSmsIntercepted());
    }

    private static class DummySmsStorage implements SmsStorage {
        private int last = -1;
        private boolean first = true;

        @Override
        public void updateLastSmsIntercepted(int smsId) {
            this.last = smsId;
            this.first = false;
        }

        @Override
        public int getLastSmsIntercepted() {
            return last;
        }

        @Override
        public boolean isFirstSmsIntercepted() {
            return first;
        }
    }
}