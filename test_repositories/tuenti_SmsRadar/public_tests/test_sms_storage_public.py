from src.smsradar.sms import Sms, SmsType
from src.smsradar.sms_storage import SmsStorage

def test_store_and_get_single_sms():
    smsStorage = SmsStorage()
    sms = Sms("Charlie", "+1987654321", "Hey there!", 1357924680, SmsType.INBOX)
    smsStorage.storeSms(sms)
    retrieved = smsStorage.getAllSms()
    assert len(retrieved) == 1
    out = retrieved[0]
    assert out.getContact() == "Charlie"
    assert out.getAddress() == "+1987654321"
    assert out.getMessage() == "Hey there!"

def test_store_multiple_sms():
    smsStorage = SmsStorage()
    s1 = Sms("Delta", "+1234509876", "First msg", 1000000100, SmsType.SENT)
    s2 = Sms("Echo", "+1987654322", "Second msg", 1000000200, SmsType.OUTBOX)
    smsStorage.storeSms(s1)
    smsStorage.storeSms(s2)
    l = smsStorage.getAllSms()
    assert len(l) == 2
    assert l[0].getMessage() == "First msg"
    assert l[1].getMessage() == "Second msg"

def test_storage_is_cleared():
    smsStorage = SmsStorage()
    smsStorage.storeSms(Sms("Foxtrot", "+1324354657", "To clear", 1234000000, SmsType.DRAFT))
    smsStorage.clearAll()
    assert len(smsStorage.getAllSms()) == 0