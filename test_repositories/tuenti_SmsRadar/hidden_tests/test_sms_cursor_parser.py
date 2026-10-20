from src.smsradar.sms import Sms, SmsType
from src.smsradar.sms_cursor_parser import SmsCursorParser
import pytest

def test_should_not_parse_any_sms_with_none():
    assert SmsCursorParser.parse(None) == []

def test_should_parse_single_sms_row():
    rows = [
        ["address", "body", "contact", "123456789", "1"]
    ]
    smses = SmsCursorParser.parse(rows)
    assert len(smses) == 1
    sms = smses[0]
    assert sms.getAddress() == "address"
    assert sms.getMessage() == "body"
    assert sms.getContact() == "contact"
    assert sms.getTime() == 123456789
    assert sms.getType() == SmsType.RECEIVED

def test_should_parse_multiple_rows_and_types():
    rows = [
        ["a", "b", "c", "1", "1"],
        ["x", "y", "z", "2", "2"]
    ]
    smses = SmsCursorParser.parse(rows)
    assert len(smses) == 2
    assert smses[0].getType() == SmsType.RECEIVED
    assert smses[1].getType() == SmsType.SENT

def test_should_handle_unknown_type():
    rows = [
        ["a", "b", "c", "3", "99"]
    ]
    smses = SmsCursorParser.parse(rows)
    assert smses[0].getType() == SmsType.UNKNOWN