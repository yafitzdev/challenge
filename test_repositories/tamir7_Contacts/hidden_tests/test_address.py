import pytest
from src.contacts.address import Address


def test_getters_and_constructors_type():
    a = Address("addr", "str", "city", "reg", "zip", "country", Address.Type.HOME)
    assert a.getFormattedAddress() == "addr"
    assert a.getStreet() == "str"
    assert a.getCity() == "city"
    assert a.getRegion() == "reg"
    assert a.getPostcode() == "zip"
    assert a.getCountry() == "country"
    assert a.getLabel() is None
    assert a.getType() == Address.Type.HOME

def test_getters_and_constructors_label():
    a = Address("addr", "str", "city", "reg", "zip", "country", "myLabel")
    assert a.getLabel() == "myLabel"
    assert a.getType() == Address.Type.CUSTOM

def test_type_from_value():
    assert Address.Type.from_value(0) == Address.Type.CUSTOM
    assert Address.Type.from_value(1) == Address.Type.HOME
    assert Address.Type.from_value(2) == Address.Type.WORK
    assert Address.Type.from_value(3) == Address.Type.OTHER
    assert Address.Type.from_value(99) == Address.Type.UNKNOWN