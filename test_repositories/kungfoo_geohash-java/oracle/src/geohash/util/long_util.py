from .._java import to_long, shl


class LongUtil:
    FIRST_BIT = to_long(0x8000000000000000)

    @staticmethod
    def common_prefix_length(a, b):
        a = to_long(a)
        b = to_long(b)
        result = 0
        while result < 64 and (a & LongUtil.FIRST_BIT) == (b & LongUtil.FIRST_BIT):
            result += 1
            a = shl(a, 1)
            b = shl(b, 1)
        return result
