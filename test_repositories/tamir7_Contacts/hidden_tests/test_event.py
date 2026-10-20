import pytest
from src.contacts.event import Event


def test_constructors_and_getters_type():
    e = Event("2023-01-01", Event.Type.BIRTHDAY)
    assert e.getStartDate() == "2023-01-01"
    assert e.getType() == Event.Type.BIRTHDAY
    assert e.getLabel() is None

def test_constructors_and_getters_label():
    e = Event("2023-01-01", "Anniversary")
    assert e.getStartDate() == "2023-01-01"
    assert e.getType() == Event.Type.CUSTOM
    assert e.getLabel() == "Anniversary"

def test_equals_and_hashcode():
    e1 = Event("2020-10-10", Event.Type.BIRTHDAY)
    e2 = Event("2020-10-10", Event.Type.BIRTHDAY)
    e3 = Event("2020-10-10", "CustomEvt")
    assert e1 == e2
    assert e1 != e3
    assert hash(e1) == hash(e2)

def test_type_from_value():
    assert Event.Type.from_value(0) == Event.Type.CUSTOM
    assert Event.Type.from_value(1) == Event.Type.ANNIVERSARY
    assert Event.Type.from_value(2) == Event.Type.OTHER
    assert Event.Type.from_value(3) == Event.Type.BIRTHDAY
    assert Event.Type.from_value(99) == Event.Type.UNKNOWN

def test_not_equal_conditions():
    e1 = Event("d", Event.Type.BIRTHDAY)
    assert e1 != None
    assert e1 != "notAnEvent"
    e2 = Event("other", Event.Type.BIRTHDAY)
    assert e1 != e2