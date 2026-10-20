"""Port of java.util.Random and Collections.shuffle(List, Random)."""

_MULT = 0x5DEECE66D
_ADD = 0xB
_MASK = (1 << 48) - 1


class JavaRandom:
    def __init__(self, seed):
        self._seed = (seed ^ _MULT) & _MASK

    def _next(self, bits):
        self._seed = (self._seed * _MULT + _ADD) & _MASK
        r = self._seed >> (48 - bits)
        if r & (1 << 31):
            r -= 1 << 32
        return r

    def next_int(self, bound):
        if bound <= 0:
            raise ValueError("bound must be positive")
        if (bound & -bound) == bound:
            return (bound * self._next(31)) >> 31
        while True:
            bits = self._next(31)
            val = bits % bound
            if bits - val + (bound - 1) < (1 << 31):
                return val


def java_shuffle(lst, rnd):
    for i in range(len(lst), 1, -1):
        j = rnd.next_int(i)
        lst[i - 1], lst[j] = lst[j], lst[i - 1]
