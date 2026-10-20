from src.smsradar.sms import Sms, SmsType

def test_constructor_and_getters_different_data():
    sms = Sms("PublicTestContact", "+10987654321", "Hello Public Test!", 1440000000, SmsType.DRAFT)
    assert sms.getContact() == "PublicTestContact"
    assert sms.getAddress() == "+10987654321"
    assert sms.getMessage() == "Hello Public Test!"
    assert sms.getTime() == 1440000000
    assert sms.getType() == SmsType.DRAFT

def test_sms_equals_different_data():
    sms1 = Sms("AA", "BB", "CC", 55555555, SmsType.OUTBOX)
    sms2 = Sms("AA", "BB", "CC", 55555555, SmsType.OUTBOX)
    assert sms1 == sms2

def test_sms_to_string_different_data():
    sms = Sms("XY", "ZZ", "MessageTest", 66778899, SmsType.DRAFT)
    s = str(sms)
    assert "XY" in s
    assert "ZZ" in s
    assert "MessageTest" in s
    assert "66778899" in s
    assert "DRAFT" in s