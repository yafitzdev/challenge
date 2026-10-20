from ._common import JavaEnum, java_string_hash, int32


class Email:
    class Type(JavaEnum):
        CUSTOM = 0
        HOME = 1
        WORK = 2
        OTHER = 3
        MOBILE = 4
        UNKNOWN = 5

        @classmethod
        def from_value(cls, value):
            return cls._from_mapping({0: "CUSTOM", 1: "HOME", 2: "WORK", 3: "OTHER", 4: "MOBILE"}, value)

        fromValue = from_value

    def __init__(self, address, type_or_label):
        self._address = address
        if isinstance(type_or_label, Email.Type):
            self._type = type_or_label
            self._label = None
        else:
            self._type = Email.Type.CUSTOM
            self._label = type_or_label

    def getAddress(self):
        return self._address

    def getType(self):
        return self._type

    def getLabel(self):
        return self._label

    def __eq__(self, o):
        if self is o:
            return True
        if o is None or type(self) is not type(o):
            return False
        return self._address == o._address and self._type is o._type and self._label == o._label

    def __ne__(self, o):
        return not self.__eq__(o)

    def __hash__(self):
        result = java_string_hash(self._address)
        result = int32(31 * result + hash(self._type))
        result = int32(31 * result + (java_string_hash(self._label) if self._label is not None else 0))
        return result

    hashCode = __hash__
    equals = __eq__
