import pytest
from src.bluetoothlegatt.sample_gatt_attributes import SampleGattAttributes

def test_lookup_null_uuid_returns_alternate_default():
    assert SampleGattAttributes.lookup(None, "alt-default") == "alt-default"

def test_lookup_empty_uuid_returns_another_default():
    assert SampleGattAttributes.lookup("", "no-value") == "no-value"

def test_lookup_null_default_returns_null_for_another_unknown():
    assert SampleGattAttributes.lookup("another-notfound-uuid", None) is None