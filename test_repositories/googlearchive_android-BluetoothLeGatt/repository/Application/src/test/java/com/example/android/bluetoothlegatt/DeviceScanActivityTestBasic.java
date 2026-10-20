package com.example.android.bluetoothlegatt;

import org.junit.Test;
import static org.junit.Assert.*;

public class DeviceScanActivityTestBasic {
    @Test
    public void scan_period_is_10000() {
        // Use reflection because it's private and final
        try {
            java.lang.reflect.Field f = DeviceScanActivity.class.getDeclaredField("SCAN_PERIOD");
            f.setAccessible(true);
            long period = f.getLong(null);
            assertEquals(10000L, period);
        } catch (Exception e) {
            fail(e.getMessage());
        }
    }
}