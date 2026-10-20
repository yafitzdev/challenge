from src.smsradar.sms import Sms, SmsType
from src.smsradar.sms_listener import SmsListener

def test_on_sms_received_callback_diff_data():
    state = {}
    class Listener(SmsListener):
        def onSmsReceived(self, sms):
            assert sms.getContact() == "ObserverName"
            assert sms.getAddress() == "+999999999"
            assert sms.getMessage() == "ObserverMsg"
            state["trigger"] = True

    listener = Listener()
    sms = Sms("ObserverName", "+999999999", "ObserverMsg", 1987654321, SmsType.SENT)
    listener.onSmsReceived(sms)
    assert state.get("trigger") == True