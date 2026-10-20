import pytest
from src.bluetoothlegatt.sample_gatt_attributes import SampleGattAttributes

def test_lookup_null_uuid_returns_default():
    assert SampleGattAttributes.lookup(None, "default") == "default"

def test_lookup_empty_uuid_returns_default():
    assert SampleGattAttributes.lookup("", "empty") == "empty"

def test_lookup_null_default_returns_null_for_unknown():
    assert SampleGattAttributes.lookup("notfound-uuid", None) is None