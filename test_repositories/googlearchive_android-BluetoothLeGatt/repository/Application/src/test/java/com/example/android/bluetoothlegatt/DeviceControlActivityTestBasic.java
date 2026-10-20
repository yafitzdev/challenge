package com.example.android.bluetoothlegatt;

import org.junit.Test;
import static org.junit.Assert.*;

public class DeviceControlActivityTestBasic {
    @Test
    public void extras_constants_are_not_null() {
        assertNotNull(DeviceControlActivity.EXTRAS_DEVICE_NAME);
        assertNotNull(DeviceControlActivity.EXTRAS_DEVICE_ADDRESS);
    }
}