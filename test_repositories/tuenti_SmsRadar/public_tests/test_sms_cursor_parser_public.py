from src.smsradar.sms import Sms, SmsType
from src.smsradar.sms_cursor_parser import SmsCursorParser

def test_parse_single_sms_row():
    rows = [
        ["+3450000000", "Text from Eve", "Eve", "1600000000000", "3"]  # INBOX for the example, or DRAFT
    ]
    smses = SmsCursorParser.parse(rows)
    assert len(smses) == 1
    sms = smses[0]
    assert sms.getAddress() == "+3450000000"
    assert sms.getMessage() == "Text from Eve"
    assert sms.getContact() == "Eve"
    assert sms.getTime() == 1600000000000
    assert sms.getType() == SmsType.DRAFT

def test_parse_multiple_sms_rows():
    rows = [
        ["123", "Bulk1", "A", "1600001", "1"],  # RECEIVED
        ["456", "Bulk2", "B", "1600002", "2"]   # SENT
    ]
    smses = SmsCursorParser.parse(rows)
    assert len(smses) == 2
    assert smses[0].getMessage() == "Bulk1"
    assert smses[1].getType() == SmsType.SENT