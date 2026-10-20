import pytest
from src.bluetoothlegatt.sample_gatt_attributes import SampleGattAttributes

def test_lookup_returns_correct_name_for_known_service():
    uuid = "0000180d-0000-1000-8000-00805f9b34fb"
    expected = "Heart Rate Service"
    assert SampleGattAttributes.lookup(uuid, "Default") == expected

def test_lookup_returns_correct_name_for_known_characteristic():
    uuid = SampleGattAttributes.HEART_RATE_MEASUREMENT
    expected = "Heart Rate Measurement"
    assert SampleGattAttributes.lookup(uuid, "None") == expected

def test_lookup_returns_default_for_unknown_uuid():
    result = SampleGattAttributes.lookup("some-unknown-uuid", "MyDefault")
    assert result == "MyDefault"

def test_lookup_distinct_for_manufacturer_name_string():
    uuid = "00002a29-0000-1000-8000-00805f9b34fb"
    assert SampleGattAttributes.lookup(uuid, "None") == "Manufacturer Name String"

def test_lookup_device_information_service():
    uuid = "0000180a-0000-1000-8000-00805f9b34fb"
    expected = "Device Information Service"
    assert SampleGattAttributes.lookup(uuid, "Unknown") == expected