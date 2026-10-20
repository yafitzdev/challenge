"""Port of com.aventrix.jnanoid.jnanoid.NanoIdUtils."""
import math
import random as _random


class NanoIdUtils:
    """A class for generating unique String IDs (port of JNanoID)."""

    DEFAULT_NUMBER_GENERATOR = _random.SystemRandom()
    DEFAULT_ALPHABET = list("_-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    DEFAULT_SIZE = 21

    def __init__(self):
        # Java constructor is private and does nothing.
        pass

    @staticmethod
    def _next_bytes(rng, n):
        if hasattr(rng, "randbytes"):
            try:
                return rng.randbytes(n)
            except NotImplementedError:
                pass
        return bytes(rng.getrandbits(8) for _ in range(n))

    @staticmethod
    def _floor_log2_shift(n):
        # Emulates (int) Math.floor(Math.log(n) / Math.log(2)) followed by Java's
        # int shift semantics (shift distance taken mod 32).
        if n <= 0:
            # Math.log(0) = -Infinity -> (int) cast gives Integer.MIN_VALUE
            k = -2147483648
        else:
            k = int(math.floor(math.log(n) / math.log(2)))
        return k & 31

    @staticmethod
    def randomNanoId(random=None, alphabet=None, size=None, *args):
        if random is None and alphabet is None and size is None:
            return NanoIdUtils.randomNanoId(
                NanoIdUtils.DEFAULT_NUMBER_GENERATOR,
                NanoIdUtils.DEFAULT_ALPHABET,
                NanoIdUtils.DEFAULT_SIZE,
            )

        if random is None:
            raise ValueError("random cannot be null.")
        if alphabet is None:
            raise ValueError("alphabet cannot be null.")
        if len(alphabet) == 0 or len(alphabet) >= 256:
            raise ValueError("alphabet must contain between 1 and 255 symbols.")
        if size is None or size <= 0:
            raise ValueError("size must be greater than zero.")

        alphabet = list(alphabet)
        n = len(alphabet)
        mask = ((2 << NanoIdUtils._floor_log2_shift(n - 1)) & 0xFFFFFFFF) - 1
        step = int(math.ceil(1.6 * mask * size / n))

        out = []
        while True:
            data = NanoIdUtils._next_bytes(random, step)
            for i in range(step):
                idx = data[i] & mask
                if idx < n:
                    out.append(alphabet[idx])
                    if len(out) == size:
                        return "".join(out)

    random_nano_id = randomNanoId
