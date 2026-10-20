package com.example.android.bluetoothlegatt;

import org.junit.Test;
import static org.junit.Assert.*;

public class SampleGattAttributesPublicTest {

    @Test
    public void lookup_returns_correct_name_for_another_known_service() {
        // Use a different service, e.g., Device Information Service
        String uuid = "0000180a-0000-1000-8000-00805f9b34fb";
        String expected = "Device Information Service";
        assertEquals(expected, SampleGattAttributes.lookup(uuid, "DefaultValue"));
    }

    @Test
    public void lookup_returns_correct_name_for_another_known_characteristic() {
        // Use Manufacturer Name String characteristic, which is different
        String uuid = "00002a29-0000-1000-8000-00805f9b34fb";
        String expected = "Manufacturer Name String";
        assertEquals(expected, SampleGattAttributes.lookup(uuid, "OtherDefault"));
    }

    @Test
    public void lookup_returns_default_for_different_unknown_uuid() {
        String result = SampleGattAttributes.lookup("unknown-public-uuid", "OtherDefaultValue");
        assertEquals("OtherDefaultValue", result);
    }

    @Test
    public void lookup_distinct_for_heart_rate_measurement() {
        // Labelling this as distinct - test the Heart Rate Measurement characteristic
        String uuid = SampleGattAttributes.HEART_RATE_MEASUREMENT;
        assertEquals("Heart Rate Measurement", SampleGattAttributes.lookup(uuid, "UnknownValue"));
    }

    @Test
    public void lookup_heart_rate_service() {
        // Use Heart Rate Service, but with a new default value
        String uuid = "0000180d-0000-1000-8000-00805f9b34fb";
        String expected = "Heart Rate Service";
        assertEquals(expected, SampleGattAttributes.lookup(uuid, "NewUnknown"));
    }
}