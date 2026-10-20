import pytest
from src.contacts.email import Email


def test_constructors_and_getters_type():
    e = Email("test@public.com", Email.Type.HOME)
    assert e.getAddress() == "test@public.com"
    assert e.getType() == Email.Type.HOME
    assert e.getLabel() is None

def test_constructors_and_getters_label():
    e = Email("alpha@beta.com", "office")
    assert e.getAddress() == "alpha@beta.com"
    assert e.getType() == Email.Type.CUSTOM
    assert e.getLabel() == "office"

def test_equals_and_hashcode():
    e1 = Email("unique@mail.com", Email.Type.MOBILE)
    e2 = Email("unique@mail.com", Email.Type.MOBILE)
    e3 = Email("unique@mail.com", "project")
    assert e1 == e2
    assert e1 != e3
    assert hash(e1) == hash(e2)

def test_type_from_value():
    assert Email.Type.from_value(-1) == Email.Type.CUSTOM  # Custom is usually 0, try -1
    assert Email.Type.from_value(1) == Email.Type.HOME
    assert Email.Type.from_value(2) == Email.Type.WORK
    assert Email.Type.from_value(3) == Email.Type.OTHER
    assert Email.Type.from_value(4) == Email.Type.MOBILE
    assert Email.Type.from_value(123) == Email.Type.UNKNOWN

def test_not_equal_conditions():
    e1 = Email("nobody@nowhere.com", Email.Type.MOBILE)
    assert e1 != None
    assert e1 != "NotAnEmailObject"
    e2 = Email("someone@somewhere.com", Email.Type.MOBILE)
    assert e1 != e2