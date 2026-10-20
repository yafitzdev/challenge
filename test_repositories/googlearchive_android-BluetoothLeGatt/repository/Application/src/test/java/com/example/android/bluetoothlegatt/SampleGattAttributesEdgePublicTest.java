package com.example.android.bluetoothlegatt;

import org.junit.Test;
import static org.junit.Assert.*;

public class SampleGattAttributesEdgePublicTest {

    @Test
    public void lookup_null_uuid_returns_alternate_default() {
        assertEquals("alt-default", SampleGattAttributes.lookup(null, "alt-default"));
    }

    @Test
    public void lookup_empty_uuid_returns_another_default() {
        assertEquals("no-value", SampleGattAttributes.lookup("", "no-value"));
    }

    @Test
    public void lookup_null_default_returns_null_for_another_unknown() {
        assertNull(SampleGattAttributes.lookup("another-notfound-uuid", null));
    }
}