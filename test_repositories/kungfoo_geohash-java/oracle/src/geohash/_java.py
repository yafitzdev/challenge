"""Helpers emulating Java primitive semantics (64-bit long, 32-bit int, Double.toString)."""
import math
import struct

MASK64 = (1 << 64) - 1


def to_long(v):
    v &= MASK64
    return v - (1 << 64) if v >= (1 << 63) else v


def to_int(v):
    v &= 0xFFFFFFFF
    return v - (1 << 32) if v >= (1 << 31) else v


def shl(v, n):
    """Java long <<"""
    return to_long(v << (n & 63))


def ushr(v, n):
    """Java long >>>"""
    return to_long((v & MASK64) >> (n & 63))


def sar(v, n):
    """Java long >>"""
    return to_long(v) >> (n & 63)


def double_to_long_bits(d):
    if d != d:
        return 0x7ff8000000000000
    return struct.unpack(">q", struct.pack(">d", float(d)))[0]


def double_hash(d):
    bits = double_to_long_bits(d)
    return to_int(bits ^ ushr(bits, 32))


def java_double_to_string(d):
    d = float(d)
    if d != d:
        return "NaN"
    if d == math.inf:
        return "Infinity"
    if d == -math.inf:
        return "-Infinity"
    if d == 0.0:
        return "-0.0" if math.copysign(1.0, d) < 0 else "0.0"
    sign = "-" if d < 0 else ""
    a = abs(d)
    r = repr(a)
    # obtain shortest digits and exponent
    mant, _, exp = r.partition("e")
    exp = int(exp) if exp else 0
    if "." in mant:
        ip, fp = mant.split(".")
    else:
        ip, fp = mant, ""
    digits = (ip + fp).lstrip("0")
    point = len(ip) + exp  # position of decimal point relative to start of ip+fp
    lead_zeros = len(ip + fp) - len((ip + fp).lstrip("0"))
    point -= lead_zeros
    digits = digits.rstrip("0") or "0"
    if 1e-3 <= a < 1e7:
        if point <= 0:
            s = "0." + "0" * (-point) + digits
        elif point >= len(digits):
            s = digits + "0" * (point - len(digits)) + ".0"
        else:
            s = digits[:point] + "." + digits[point:]
        return sign + s
    e = point - 1
    frac = digits[1:] or "0"
    return sign + digits[0] + "." + frac + "E" + str(e)


class JavaRandom:
    """Port of java.util.Random (48-bit LCG)."""
    _MULT = 0x5DEECE66D
    _ADD = 0xB
    _MASK = (1 << 48) - 1

    def __init__(self, seed=None):
        if seed is None:
            import os
            seed = int.from_bytes(os.urandom(8), "big")
        self._seed = (seed ^ self._MULT) & self._MASK

    def _next(self, bits):
        self._seed = (self._seed * self._MULT + self._ADD) & self._MASK
        return to_int(self._seed >> (48 - bits))

    def next_int(self, bound=None):
        if bound is None:
            return self._next(32)
        if bound <= 0:
            raise ValueError("bound must be positive")
        if (bound & -bound) == bound:
            return to_int((bound * self._next(31)) >> 31)
        while True:
            bits = self._next(31)
            val = bits % bound
            if to_int(bits - val + (bound - 1)) >= 0:
                return val

    def next_double(self):
        return ((self._next(26) << 27) + self._next(27)) * (1.0 / (1 << 53))
