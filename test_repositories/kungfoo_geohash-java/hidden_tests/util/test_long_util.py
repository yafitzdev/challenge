from src.geohash.util.long_util import LongUtil

def test_common_prefix_length():
    # Same value
    assert LongUtil.common_prefix_length(0x123456789abcdef0, 0x123456789abcdef0) == 64
    # Differs at first bit
    assert LongUtil.common_prefix_length(0x0000000000000000, 0x8000000000000000) == 0
    # Differs at last bit
    assert LongUtil.common_prefix_length(0x8000000000000001, 0x8000000000000000) == 63
    # No match at all
    assert LongUtil.common_prefix_length(0, 0xFFFFFFFFFFFFFFFF) == 0