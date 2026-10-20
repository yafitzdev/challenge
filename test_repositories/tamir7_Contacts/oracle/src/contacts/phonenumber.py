from ._common import JavaEnum, java_string_hash, int32

_PHONE_TYPES = [
    "CUSTOM", "HOME", "MOBILE", "WORK", "FAX_WORK", "FAX_HOME", "PAGER", "OTHER",
    "CALLBACK", "CAR", "COMPANY_MAIN", "ISDN", "MAIN", "OTHER_FAX", "RADIO", "TELEX",
    "TTY_TDD", "WORK_MOBILE", "WORK_PAGER", "ASSISTANT", "MMS",
]


class PhoneNumber:
    class Type(JavaEnum):
        CUSTOM = 0
        HOME = 1
        MOBILE = 2
        WORK = 3
        FAX_WORK = 4
        FAX_HOME = 5
        PAGER = 6
        OTHER = 7
        CALLBACK = 8
        CAR = 9
        COMPANY_MAIN = 10
        ISDN = 11
        MAIN = 12
        OTHER_FAX = 13
        RADIO = 14
        TELEX = 15
        TTY_TDD = 16
        WORK_MOBILE = 17
        WORK_PAGER = 18
        ASSISTANT = 19
        MMS = 20
        UNKNOWN = 21

        @classmethod
        def from_value(cls, value):
            # ContactsContract.CommonDataKinds.Phone TYPE_* constants (0..20)
            return cls._from_mapping(dict(enumerate(_PHONE_TYPES)), value)

        fromValue = from_value

    def __init__(self, number, type_or_label, normalized_number):
        self._number = number
        if isinstance(type_or_label, PhoneNumber.Type):
            self._type = type_or_label
            self._label = None
        else:
            self._type = PhoneNumber.Type.CUSTOM
            self._label = type_or_label
        self._normalized_number = normalized_number

    def getNumber(self):
        return self._number

    def getLabel(self):
        return self._label

    def getNormalizedNumber(self):
        return self._normalized_number

    def getType(self):
        return self._type

    def __eq__(self, o):
        if self is o:
            return True
        if o is None or type(self) is not type(o):
            return False
        return (self._number == o._number and self._type is o._type
                and self._label == o._label and self._normalized_number == o._normalized_number)

    def __ne__(self, o):
        return not self.__eq__(o)

    def __hash__(self):
        result = java_string_hash(self._number)
        result = int32(31 * result + hash(self._type))
        result = int32(31 * result + (java_string_hash(self._label) if self._label is not None else 0))
        result = int32(31 * result + (java_string_hash(self._normalized_number)
                                      if self._normalized_number is not None else 0))
        return result

    hashCode = __hash__
    equals = __eq__
