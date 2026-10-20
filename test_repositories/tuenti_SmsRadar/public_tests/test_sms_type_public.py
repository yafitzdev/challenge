from src.smsradar.sms import SmsType

def test_value_of():
    type1 = SmsType["INBOX"]
    assert type1 == SmsType.INBOX
    type2 = SmsType["SENT"]
    assert type2 == SmsType.SENT

def test_ordinal_different_from_test():
    # In Python the enum auto-generated .ordinal() does not exist, but .value does
    assert SmsType.OUTBOX.value != hash("SENT")

def test_values_array_length():
    values = list(SmsType)
    assert len(values) > 1