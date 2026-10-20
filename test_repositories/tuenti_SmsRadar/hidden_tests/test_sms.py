from src.smsradar.sms import Sms, SmsType

def test_constructor_and_getters():
    sms = Sms("12345", "1687221000000", "Hello there!", SmsType.RECEIVED)
    assert sms.getContact() == "12345"
    assert sms.getAddress() == "1687221000000"
    assert sms.getMessage() == "Hello there!"
    assert sms.getType() == SmsType.RECEIVED

def test_equals_hashcode_and_to_string():
    a = Sms("a", "111", "body", SmsType.RECEIVED)
    b = Sms("a", "111", "body", SmsType.RECEIVED)
    c = Sms("b", "112", "other", SmsType.SENT)
    assert a == b
    assert hash(a) == hash(b)
    assert a != c
    assert hash(a) != hash(c)
    assert "body" in str(a)

def test_not_equal_with_null_or_other_type():
    sms = Sms("a", "c", "b", SmsType.UNKNOWN)
    assert sms != None
    assert sms != "Some String"