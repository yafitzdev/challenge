"""Port of com.tuenti.smsradar.TimeProvider."""
import datetime


class TimeProvider(object):
    """Provides the current date (abstraction to allow mocking in tests)."""

    def getDate(self):
        return datetime.datetime.now()
