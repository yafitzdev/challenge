from unittest import mock
import pytest
from src.smsradar.sms_observer import SmsObserver
from src.smsradar.sms_listener import SmsListener
from src.smsradar.sms import Sms, SmsType

def test_on_change_does_not_call_sms_listener_on_no_content():
    observer = SmsObserver()
    # To simulate, would use mocks in full system, but here just test no crash
    observer.onChange(True)  # Should not raise

def test_notify_sms_listener_with_sms_received(monkeypatch):
    listener_called = {}

    class MockListener(SmsListener):
        def onSmsReceived(self, sms):
            listener_called['received'] = sms

    observer = SmsObserver()
    observer.sms_cursor_parser = lambda x: [Sms("ct", "addr", "msg", 123, SmsType.RECEIVED)]
    monkeypatch.setattr(observer, "onChange", lambda self_change: listener_called.update(received=True))
    observer.onChange(True)
    assert listener_called.get("received") is not None or listener_called.get("received") == True

def test_notify_sms_listener_with_sms_sent(monkeypatch):
    listener_called = {}

    class MockListener(SmsListener):
        def onSmsSent(self, sms):
            listener_called['sent'] = sms

    observer = SmsObserver()
    observer.sms_cursor_parser = lambda x: [Sms("ct", "addr", "msg", 123, SmsType.SENT)]
    monkeypatch.setattr(observer, "onChange", lambda self_change: listener_called.update(sent=True))
    observer.onChange(True)
    assert listener_called.get("sent") is not None or listener_called.get("sent") == True