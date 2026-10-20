import pytest
from src.contacts.event import Event


def test_constructors_and_getters_type():
    e = Event("2050-12-31", Event.Type.ANNIVERSARY)
    assert e.getStartDate() == "2050-12-31"
    assert e.getType() == Event.Type.ANNIVERSARY
    assert e.getLabel() is None

def test_constructors_and_getters_label():
    e = Event("2024-07-14", "Special Date")
    assert e.getStartDate() == "2024-07-14"
    assert e.getType() == Event.Type.CUSTOM
    assert e.getLabel() == "Special Date"

def test_equals_and_hashcode():
    e1 = Event("2000-01-01", Event.Type.OTHER)
    e2 = Event("2000-01-01", Event.Type.OTHER)
    e3 = Event("2000-01-01", "Anniv")
    assert e1 == e2
    assert e1 != e3
    assert hash(e1) == hash(e2)

def test_type_from_value():
    assert Event.Type.from_value(-1) == Event.Type.CUSTOM
    assert Event.Type.from_value(1) == Event.Type.ANNIVERSARY
    assert Event.Type.from_value(2) == Event.Type.OTHER
    assert Event.Type.from_value(3) == Event.Type.BIRTHDAY
    assert Event.Type.from_value(500) == Event.Type.UNKNOWN

def test_not_equal_conditions():
    e1 = Event("2029-11-11", Event.Type.OTHER)
    assert e1 != None
    assert e1 != object()
    e2 = Event("2222-02-22", Event.Type.OTHER)
    assert e1 != e2