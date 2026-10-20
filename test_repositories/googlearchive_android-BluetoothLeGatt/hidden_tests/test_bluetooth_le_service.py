import pytest
from src.bluetoothlegatt.bluetooth_le_service import BluetoothLeService

def test_static_fields_not_null():
    # All these should be present and not None
    assert BluetoothLeService.ACTION_GATT_CONNECTED is not None
    assert BluetoothLeService.ACTION_GATT_DISCONNECTED is not None
    assert BluetoothLeService.ACTION_GATT_SERVICES_DISCOVERED is not None
    assert BluetoothLeService.ACTION_DATA_AVAILABLE is not None
    assert BluetoothLeService.EXTRA_DATA is not None
    assert BluetoothLeService.UUID_HEART_RATE_MEASUREMENT is not None