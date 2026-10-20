import pytest
from src.contacts.address import Address


def test_constructors_and_getters_type():
    a = Address("Street 123", "Townsville", "AA", "CountryX", "98765", Address.Type.WORK)
    assert a.getStreet() == "Street 123"
    assert a.getCity() == "Townsville"
    assert a.getRegion() == "AA"
    assert a.getCountry() == "CountryX"
    assert a.getPostalCode() == "98765"
    assert a.getType() == Address.Type.WORK
    assert a.getLabel() is None

def test_constructors_and_getters_label():
    a = Address("Ave A", "Metropolis", "BB", "CountryY", "24680", "Vacation Spot")
    assert a.getStreet() == "Ave A"
    assert a.getCity() == "Metropolis"
    assert a.getRegion() == "BB"
    assert a.getCountry() == "CountryY"
    assert a.getPostalCode() == "24680"
    assert a.getType() == Address.Type.CUSTOM
    assert a.getLabel() == "Vacation Spot"

def test_equals_and_hashcode():
    a1 = Address("Zebra", "CityZ", "RR", "LandQ", "65432", Address.Type.HOME)
    a2 = Address("Zebra", "CityZ", "RR", "LandQ", "65432", Address.Type.HOME)
    a3 = Address("Zebra", "CityZ", "RR", "LandQ", "65432", "MyPlace")
    assert a1 == a2
    assert a1 != a3
    assert hash(a1) == hash(a2)

def test_type_from_value():
    assert Address.Type.from_value(-1) == Address.Type.CUSTOM
    assert Address.Type.from_value(1) == Address.Type.HOME
    assert Address.Type.from_value(2) == Address.Type.WORK
    assert Address.Type.from_value(3) == Address.Type.OTHER
    assert Address.Type.from_value(100) == Address.Type.UNKNOWN

def test_not_equal_conditions():
    a1 = Address("Alpha", "Beta", "Gamma", "Delta", "61616", Address.Type.WORK)
    assert a1 != None
    assert a1 != "NotAnAddress"
    a2 = Address("Beta", "Gamma", "Delta", "Epsilon", "89898", Address.Type.WORK)
    assert a1 != a2