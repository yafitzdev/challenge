package com.example.android.bluetoothlegatt;

import org.junit.Test;
import static org.junit.Assert.*;

public class SampleGattAttributesEdgeTest {

    @Test
    public void lookup_null_uuid_returns_default() {
        assertEquals("default", SampleGattAttributes.lookup(null, "default"));
    }

    @Test
    public void lookup_empty_uuid_returns_default() {
        assertEquals("empty", SampleGattAttributes.lookup("", "empty"));
    }

    @Test
    public void lookup_null_default_returns_null_for_unknown() {
        assertNull(SampleGattAttributes.lookup("notfound-uuid", null));
    }
}