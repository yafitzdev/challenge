"""Port of com.tuenti.smsradar.SmsCursorParser.

`cursor` is any object implementing the subset of android.database.Cursor used here:
getCount(), moveToNext(), getColumnIndex(name), getString(index), getInt(index).
"""
from .sms import Sms, SmsType


class SmsCursorParser(object):
    ADDRESS_COLUMN_NAME = "address"
    DATE_COLUMN_NAME = "date"
    BODY_COLUMN_NAME = "body"
    TYPE_COLUMN_NAME = "type"
    ID_COLUMN_NAME = "_id"
    SMS_MAX_AGE_MILLIS = 5000

    def __init__(self, sms_storage, time_provider):
        self._sms_storage = sms_storage
        self._time_provider = time_provider

    def parse(self, cursor):
        if not self._can_handle_cursor(cursor) or not cursor.moveToNext():
            return None
        sms_parsed = self._extract_sms_info_from_cursor(cursor)
        sms_id = cursor.getInt(cursor.getColumnIndex(self.ID_COLUMN_NAME))
        date = cursor.getString(cursor.getColumnIndex(self.DATE_COLUMN_NAME))
        sms_date_millis = int(date)
        if self._should_parse_sms(sms_id, sms_date_millis):
            self._sms_storage.updateLastSmsIntercepted(sms_id)
        else:
            sms_parsed = None
        return sms_parsed

    def _should_parse_sms(self, sms_id, sms_date_millis):
        is_first = self._sms_storage.isFirstSmsIntercepted()
        is_old = self._is_old(sms_date_millis)
        should_parse_id = self._should_parse_sms_id(sms_id)
        return (is_first and not is_old) or (not is_first and should_parse_id)

    def _is_old(self, sms_date_millis):
        now = self._time_provider.getDate()
        return _to_millis(now) - sms_date_millis > self.SMS_MAX_AGE_MILLIS

    def _should_parse_sms_id(self, sms_id):
        if self._sms_storage.isFirstSmsIntercepted():
            return False
        return sms_id > self._sms_storage.getLastSmsIntercepted()

    def _extract_sms_info_from_cursor(self, cursor):
        address = cursor.getString(cursor.getColumnIndex(self.ADDRESS_COLUMN_NAME))
        date = cursor.getString(cursor.getColumnIndex(self.DATE_COLUMN_NAME))
        msg = cursor.getString(cursor.getColumnIndex(self.BODY_COLUMN_NAME))
        sms_type = cursor.getString(cursor.getColumnIndex(self.TYPE_COLUMN_NAME))
        return Sms(address, date, msg, SmsType.from_value(int(sms_type)))

    @staticmethod
    def _can_handle_cursor(cursor):
        return cursor is not None and cursor.getCount() > 0


def _to_millis(date):
    if hasattr(date, "getTime"):
        return date.getTime()
    if hasattr(date, "timestamp"):
        return int(date.timestamp() * 1000)
    return int(date)
