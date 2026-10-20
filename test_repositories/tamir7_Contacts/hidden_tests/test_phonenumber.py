import pytest
from src.contacts.phonenumber import PhoneNumber


def test_constructors_and_getters_type():
    p = PhoneNumber("12345", PhoneNumber.Type.HOME, "54321")
    assert p.getNumber() == "12345"
    assert p.getNormalizedNumber() == "54321"
    assert p.getType() == PhoneNumber.Type.HOME
    assert p.getLabel() is None

def test_constructors_and_getters_label():
    p = PhoneNumber("333", "mobile label", "333")
    assert p.getNumber() == "333"
    assert p.getLabel() == "mobile label"
    assert p.getType() == PhoneNumber.Type.CUSTOM
    assert p.getNormalizedNumber() == "333"

def test_equals_and_hashcode():
    p1 = PhoneNumber("123", PhoneNumber.Type.HOME, "abc")
    p2 = PhoneNumber("123", PhoneNumber.Type.HOME, "abc")
    p3 = PhoneNumber("999", PhoneNumber.Type.HOME, "abc")
    assert p1 == p2
    assert p1 != p3
    assert hash(p1) == hash(p2)

def test_type_from_value():
    assert PhoneNumber.Type.from_value(0) == PhoneNumber.Type.CUSTOM
    assert PhoneNumber.Type.from_value(1) == PhoneNumber.Type.HOME
    assert PhoneNumber.Type.from_value(2) == PhoneNumber.Type.MOBILE
    assert PhoneNumber.Type.from_value(3) == PhoneNumber.Type.WORK
    assert PhoneNumber.Type.from_value(4) == PhoneNumber.Type.FAX_WORK
    assert PhoneNumber.Type.from_value(5) == PhoneNumber.Type.FAX_HOME
    assert PhoneNumber.Type.from_value(6) == PhoneNumber.Type.PAGER
    assert PhoneNumber.Type.from_value(7) == PhoneNumber.Type.OTHER
    assert PhoneNumber.Type.from_value(8) == PhoneNumber.Type.CALLBACK
    assert PhoneNumber.Type.from_value(9) == PhoneNumber.Type.CAR
    assert PhoneNumber.Type.from_value(10) == PhoneNumber.Type.COMPANY_MAIN
    assert PhoneNumber.Type.from_value(11) == PhoneNumber.Type.ISDN
    assert PhoneNumber.Type.from_value(12) == PhoneNumber.Type.MAIN
    assert PhoneNumber.Type.from_value(13) == PhoneNumber.Type.OTHER_FAX
    assert PhoneNumber.Type.from_value(14) == PhoneNumber.Type.RADIO
    assert PhoneNumber.Type.from_value(15) == PhoneNumber.Type.TELEX
    assert PhoneNumber.Type.from_value(16) == PhoneNumber.Type.TTY_TDD
    assert PhoneNumber.Type.from_value(17) == PhoneNumber.Type.WORK_MOBILE
    assert PhoneNumber.Type.from_value(18) == PhoneNumber.Type.WORK_PAGER
    assert PhoneNumber.Type.from_value(19) == PhoneNumber.Type.ASSISTANT
    assert PhoneNumber.Type.from_value(20) == PhoneNumber.Type.MMS
    assert PhoneNumber.Type.from_value(999) == PhoneNumber.Type.UNKNOWN

def test_not_equal_conditions():
    p1 = PhoneNumber("x", PhoneNumber.Type.HOME, "n")
    assert p1 != None
    assert p1 != "notPhone"
    p2 = PhoneNumber("different", PhoneNumber.Type.HOME, "n")
    assert p1 != p2