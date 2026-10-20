"""Port of com.tuenti.smsradar.Sms and com.tuenti.smsradar.SmsType."""
from enum import Enum


def _java_string_hash(s):
    h = 0
    for ch in s:
        h = (31 * h + ord(ch)) & 0xFFFFFFFF
    if h >= 0x80000000:
        h -= 0x100000000
    return h


class SmsType(Enum):
    UNKNOWN = -1
    RECEIVED = 1
    SENT = 2

    def getValue(self):
        return self.value

    @classmethod
    def from_value(cls, value):
        for sms_type in cls:
            if sms_type.value == value:
                return sms_type
        raise ValueError("Invalid sms type: " + str(value))

    fromValue = from_value

    @classmethod
    def valueOf(cls, name):
        return cls[name]

    def __str__(self):
        return self.name


class Sms(object):
    """Immutable SMS representation: address, date, msg and type."""

    def __init__(self, address, date, msg, type):
        self._address = address
        self._date = date
        self._msg = msg
        self._type = type

    def getAddress(self):
        return self._address

    def getDate(self):
        return self._date

    def getMsg(self):
        return self._msg

    def getType(self):
        return self._type

    def __eq__(self, o):
        if self is o:
            return True
        if not isinstance(o, Sms):
            return False
        return (self._address == o._address and self._date == o._date
                and self._msg == o._msg and self._type is o._type)

    def __ne__(self, o):
        return not self.__eq__(o)

    def hashCode(self):
        result = _java_string_hash(self._address) if self._address is not None else 0
        result = 31 * result + (_java_string_hash(self._date) if self._date is not None else 0)
        result = 31 * result + (_java_string_hash(self._msg) if self._msg is not None else 0)
        result = 31 * result + (_java_string_hash(self._type.name) if self._type is not None else 0)
        result &= 0xFFFFFFFF
        if result >= 0x80000000:
            result -= 0x100000000
        return result

    def __hash__(self):
        return self.hashCode()

    def __str__(self):
        return ("Sms{" + "address='" + str(self._address) + "'" + ", date='" + str(self._date) + "'"
                + ", msg='" + str(self._msg) + "'" + ", type=" + str(self._type) + "}")

    __repr__ = __str__
