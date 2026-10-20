from ._common import JavaEnum, java_string_hash, int32


class Event:
    class Type(JavaEnum):
        CUSTOM = 0
        ANNIVERSARY = 1
        OTHER = 2
        BIRTHDAY = 3
        UNKNOWN = 4

        @classmethod
        def from_value(cls, value):
            return cls._from_mapping({0: "CUSTOM", 1: "ANNIVERSARY", 2: "OTHER", 3: "BIRTHDAY"}, value)

        fromValue = from_value

    def __init__(self, start_date, type_or_label):
        self._start_date = start_date
        if isinstance(type_or_label, Event.Type):
            self._type = type_or_label
            self._label = None
        else:
            self._type = Event.Type.CUSTOM
            self._label = type_or_label

    def getStartDate(self):
        return self._start_date

    def getType(self):
        return self._type

    def getLabel(self):
        return self._label

    def __eq__(self, o):
        if self is o:
            return True
        if o is None or type(self) is not type(o):
            return False
        return self._start_date == o._start_date and self._type is o._type and self._label == o._label

    def __ne__(self, o):
        return not self.__eq__(o)

    def __hash__(self):
        result = java_string_hash(self._start_date)
        result = int32(31 * result + hash(self._type))
        result = int32(31 * result + (java_string_hash(self._label) if self._label is not None else 0))
        return result

    hashCode = __hash__
    equals = __eq__
