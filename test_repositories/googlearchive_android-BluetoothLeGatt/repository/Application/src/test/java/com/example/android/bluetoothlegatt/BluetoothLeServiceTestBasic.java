package com.example.android.bluetoothlegatt;

import org.junit.Test;
import static org.junit.Assert.*;

public class BluetoothLeServiceTestBasic {
    @Test
    public void testStaticFieldsNotNull() {
        assertNotNull(BluetoothLeService.ACTION_GATT_CONNECTED);
        assertNotNull(BluetoothLeService.ACTION_GATT_DISCONNECTED);
        assertNotNull(BluetoothLeService.ACTION_GATT_SERVICES_DISCOVERED);
        assertNotNull(BluetoothLeService.ACTION_DATA_AVAILABLE);
        assertNotNull(BluetoothLeService.EXTRA_DATA);
        assertNotNull(BluetoothLeService.UUID_HEART_RATE_MEASUREMENT);
    }
}