import pytest
from src.contacts.email import Email


def test_constructors_and_getters_type():
    e = Email("addr@email.com", Email.Type.WORK)
    assert e.getAddress() == "addr@email.com"
    assert e.getType() == Email.Type.WORK
    assert e.getLabel() is None

def test_constructors_and_getters_label():
    e = Email("foo@bar.com", "mylabel")
    assert e.getAddress() == "foo@bar.com"
    assert e.getType() == Email.Type.CUSTOM
    assert e.getLabel() == "mylabel"

def test_equals_and_hashcode():
    e1 = Email("x@x.com", Email.Type.HOME)
    e2 = Email("x@x.com", Email.Type.HOME)
    e3 = Email("x@x.com", "label")
    assert e1 == e2
    assert e1 != e3
    assert hash(e1) == hash(e2)

def test_type_from_value():
    assert Email.Type.from_value(0) == Email.Type.CUSTOM
    assert Email.Type.from_value(1) == Email.Type.HOME
    assert Email.Type.from_value(2) == Email.Type.WORK
    assert Email.Type.from_value(3) == Email.Type.OTHER
    assert Email.Type.from_value(4) == Email.Type.MOBILE
    assert Email.Type.from_value(99) == Email.Type.UNKNOWN

def test_not_equal_conditions():
    e1 = Email("x@x.com", Email.Type.HOME)
    assert e1 != None
    assert e1 != "notAnEmail"
    e2 = Email("z@z.com", Email.Type.HOME)
    assert e1 != e2