import pytest
from src.smsradar.sms import SmsType

def test_from_value_received():
    assert SmsType.from_value(1) == SmsType.RECEIVED

def test_from_value_sent():
    assert SmsType.from_value(2) == SmsType.SENT

def test_from_value_unknown():
    assert SmsType.from_value(-1) == SmsType.UNKNOWN

def test_from_value_invalid():
    with pytest.raises(ValueError):
        SmsType.from_value(5)

def test_sms_type_values():
    assert SmsType.UNKNOWN.value == -1
    assert SmsType.RECEIVED.value == 1
    assert SmsType.SENT.value == 2

def test_value_of_enum():
    assert SmsType['UNKNOWN'] == SmsType.UNKNOWN
    assert SmsType['RECEIVED'] == SmsType.RECEIVED
    assert SmsType['SENT'] == SmsType.SENT