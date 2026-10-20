"""Port of com.tuenti.smsradar.SharedPreferencesSmsStorage.

`preferences` must be an object implementing the subset of android.content.SharedPreferences
used here: edit() returning an editor with putInt()/commit(), and getInt(key, default).
"""
from .sms_storage import SmsStorage


class SharedPreferencesSmsStorage(SmsStorage):
    LAST_SMS_PARSED = "last_sms_parsed"
    DEFAULT_SMS_PARSED_VALUE = -1

    def __init__(self, preferences):
        if preferences is None:
            raise ValueError("SharedPreferences param can't be null")
        self._preferences = preferences

    def updateLastSmsIntercepted(self, sms_id):
        editor = self._preferences.edit()
        editor.putInt(self.LAST_SMS_PARSED, sms_id)
        editor.commit()

    def getLastSmsIntercepted(self):
        return self._preferences.getInt(self.LAST_SMS_PARSED, self.DEFAULT_SMS_PARSED_VALUE)

    def isFirstSmsIntercepted(self):
        return self.getLastSmsIntercepted() == self.DEFAULT_SMS_PARSED_VALUE
