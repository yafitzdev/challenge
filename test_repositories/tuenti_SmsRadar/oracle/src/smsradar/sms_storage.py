"""Port of the com.tuenti.smsradar.SmsStorage interface."""
from abc import ABCMeta, abstractmethod


class SmsStorage(metaclass=ABCMeta):
    """Declares the interface used to store the last SMS intercepted."""

    @abstractmethod
    def updateLastSmsIntercepted(self, sms_id):
        pass

    @abstractmethod
    def getLastSmsIntercepted(self):
        pass

    @abstractmethod
    def isFirstSmsIntercepted(self):
        pass
