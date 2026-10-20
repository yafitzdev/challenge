package com.example.android.bluetoothlegatt;

import org.junit.Test;
import static org.junit.Assert.*;

public class SampleGattAttributesTest {

    @Test
    public void lookup_returns_correct_name_for_known_service() {
        String uuid = "0000180d-0000-1000-8000-00805f9b34fb";
        String expected = "Heart Rate Service";
        assertEquals(expected, SampleGattAttributes.lookup(uuid, "Default"));
    }

    @Test
    public void lookup_returns_correct_name_for_known_characteristic() {
        String uuid = SampleGattAttributes.HEART_RATE_MEASUREMENT;
        String expected = "Heart Rate Measurement";
        assertEquals(expected, SampleGattAttributes.lookup(uuid, "None"));
    }

    @Test
    public void lookup_returns_default_for_unknown_uuid() {
        String result = SampleGattAttributes.lookup("some-unknown-uuid", "MyDefault");
        assertEquals("MyDefault", result);
    }

    @Test
    public void lookup_distinct_for_manufacturer_name_string() {
        String uuid = "00002a29-0000-1000-8000-00805f9b34fb";
        assertEquals("Manufacturer Name String", SampleGattAttributes.lookup(uuid, "None"));
    }

    @Test
    public void lookup_device_information_service() {
        String uuid = "0000180a-0000-1000-8000-00805f9b34fb";
        String expected = "Device Information Service";
        assertEquals(expected, SampleGattAttributes.lookup(uuid, "Unknown"));
    }
}