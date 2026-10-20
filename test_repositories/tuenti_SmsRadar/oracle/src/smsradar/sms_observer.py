"""Port of com.tuenti.smsradar.SmsObserver (an android ContentObserver)."""
from .sms import SmsType
from .sms_radar import SmsRadar


class SmsObserver(object):
    SMS_URI = "content://sms/"
    SMS_SENT_URI = "content://sms/sent"
    SMS_INBOX_URI = "content://sms/inbox"
    PROTOCOL_COLUM_NAME = "protocol"
    SMS_ORDER = "date DESC"

    def __init__(self, content_resolver=None, handler=None, sms_cursor_parser=None):
        self._handler = handler
        self.content_resolver = content_resolver
        self.sms_cursor_parser = sms_cursor_parser

    def deliverSelfNotifications(self):
        return True

    def onChange(self, self_change):
        cursor = None
        try:
            cursor = self._get_sms_content_observer_cursor()
            if cursor is not None and cursor.moveToFirst():
                self._process_sms(cursor)
        finally:
            self._close(cursor)

    def _process_sms(self, cursor):
        sms_cursor = None
        try:
            protocol = cursor.getString(cursor.getColumnIndex(self.PROTOCOL_COLUM_NAME))
            sms_cursor = self._get_sms_details_cursor_for_protocol(protocol)
            sms = self.sms_cursor_parser.parse(sms_cursor)
            self._notify_sms_listener(sms)
        finally:
            self._close(sms_cursor)

    @staticmethod
    def _notify_sms_listener(sms):
        listener = SmsRadar.smsListener
        if sms is not None and listener is not None:
            if sms.getType() is SmsType.SENT:
                listener.onSmsSent(sms)
            else:
                listener.onSmsReceived(sms)

    def _get_sms_details_cursor_for_protocol(self, protocol):
        if protocol is None:
            return self._get_sms_details_cursor(self.SMS_SENT_URI)
        return self._get_sms_details_cursor(self.SMS_INBOX_URI)

    def _get_sms_content_observer_cursor(self):
        return self.content_resolver.query(self.SMS_URI, None, None, None, None)

    def _get_sms_details_cursor(self, sms_uri):
        return self.content_resolver.query(sms_uri, None, None, None, self.SMS_ORDER) \
            if sms_uri is not None else None

    @staticmethod
    def _close(cursor):
        if cursor is not None:
            cursor.close()
