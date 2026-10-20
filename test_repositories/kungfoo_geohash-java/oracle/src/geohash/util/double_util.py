import math


class DoubleUtil:
    @staticmethod
    def remainder_with_fix(value, remainder):
        res = math.fmod(float(value), remainder)  # Java % semantics
        return res + remainder if res < 0 else res
