from src.smsradar.sms import Sms, SmsType
from src.smsradar.sms_storage import SmsStorage

def test_is_first_sms_intercepted_initially_true():
    class DummySmsStorage:
        def __init__(self):
            self.last = -1
            self.first = True

        def updateLastSmsIntercepted(self, sms_id):
            self.last = sms_id
            self.first = False

        def getLastSmsIntercepted(self):
            return self.last

        def isFirstSmsIntercepted(self):
            return self.first

    storage = DummySmsStorage()
    assert storage.isFirstSmsIntercepted()

def test_update_and_get_last_sms():
    class DummySmsStorage:
        def __init__(self):
            self.last = -1
            self.first = True

        def updateLastSmsIntercepted(self, sms_id):
            self.last = sms_id
            self.first = False

        def getLastSmsIntercepted(self):
            return self.last

        def isFirstSmsIntercepted(self):
            return self.first

    storage = DummySmsStorage()
    storage.updateLastSmsIntercepted(42)
    assert not storage.isFirstSmsIntercepted()
    assert storage.getLastSmsIntercepted() == 42

def test_add_and_get_all_sms():
    storage = SmsStorage()
    sms1 = Sms("1", "111", "msg1", SmsType.RECEIVED)
    sms2 = Sms("2", "222", "msg2", SmsType.SENT)
    storage.addSms(sms1)
    storage.addSms(sms2)
    all_sms = storage.getAllSms()
    assert len(all_sms) == 2
    assert sms1 in all_sms
    assert sms2 in all_sms

def test_clear_storage():
    storage = SmsStorage()
    sms = Sms("1", "111", "msg1", SmsType.RECEIVED)
    storage.addSms(sms)
    storage.clear()
    assert len(storage.getAllSms()) == 0

def test_store_and_get_all_sms_public():
    storage = SmsStorage()
    sms1 = Sms("Alpha", "+100", "happy", SmsType.SENT)
    storage.storeSms(sms1)
    out = storage.getAllSms()
    assert out[0] == sms1

def test_clear_all_clears_sms_public():
    storage = SmsStorage()
    storage.storeSms(Sms("X", "Y", "Z", SmsType.INBOX))
    storage.clearAll()
    assert len(storage.getAllSms()) == 0