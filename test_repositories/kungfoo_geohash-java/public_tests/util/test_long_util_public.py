from src.geohash.util.long_util import LongUtil

def test_common_prefix_length_public():
    assert LongUtil.common_prefix_length(0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF) == 64
    assert LongUtil.common_prefix_length(0x4000000000000000, 0xC000000000000000) == 1
    assert LongUtil.common_prefix_length(0x80000000FFFFFFFF, 0x800000007FFFFFFF) == 31