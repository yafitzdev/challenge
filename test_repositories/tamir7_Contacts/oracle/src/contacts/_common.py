from enum import Enum


def java_string_hash(s):
    h = 0
    for ch in s:
        h = (31 * h + ord(ch)) & 0xFFFFFFFF
    return h - (1 << 32) if h >= (1 << 31) else h


def int32(v):
    v &= 0xFFFFFFFF
    return v - (1 << 32) if v >= (1 << 31) else v


class JavaEnum(Enum):
    """Enum whose members are declared in Java ordinal order."""

    @classmethod
    def _from_mapping(cls, mapping, value):
        name = mapping.get(value)
        return cls[name] if name is not None else cls.UNKNOWN
