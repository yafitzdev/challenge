import pytest
from src.bluetoothlegatt.sample_gatt_attributes import SampleGattAttributes

def test_lookup_returns_correct_name_for_another_known_service():
    uuid = "0000180a-0000-1000-8000-00805f9b34fb"
    expected = "Device Information Service"
    assert SampleGattAttributes.lookup(uuid, "DefaultValue") == expected

def test_lookup_returns_correct_name_for_another_known_characteristic():
    uuid = "00002a29-0000-1000-8000-00805f9b34fb"
    expected = "Manufacturer Name String"
    assert SampleGattAttributes.lookup(uuid, "OtherDefault") == expected

def test_lookup_returns_default_for_different_unknown_uuid():
    result = SampleGattAttributes.lookup("unknown-public-uuid", "OtherDefaultValue")
    assert result == "OtherDefaultValue"

def test_lookup_distinct_for_heart_rate_measurement():
    uuid = SampleGattAttributes.HEART_RATE_MEASUREMENT
    assert SampleGattAttributes.lookup(uuid, "UnknownValue") == "Heart Rate Measurement"

def test_lookup_heart_rate_service():
    uuid = "0000180d-0000-1000-8000-00805f9b34fb"
    expected = "Heart Rate Service"
    assert SampleGattAttributes.lookup(uuid, "NewUnknown") == expected