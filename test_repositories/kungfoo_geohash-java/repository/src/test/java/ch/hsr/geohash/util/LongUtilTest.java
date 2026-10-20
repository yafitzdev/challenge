package ch.hsr.geohash.util;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class LongUtilTest {
    @Test
    public void testCommonPrefixLength() {
        // Same value
        assertEquals(64, LongUtil.commonPrefixLength(0x123456789abcdef0L, 0x123456789abcdef0L));
        // Differs at first bit
        assertEquals(0, LongUtil.commonPrefixLength(0x0000000000000000L, 0x8000000000000000L));
        // Differs at last bit
        assertEquals(63, LongUtil.commonPrefixLength(0x8000000000000001L, 0x8000000000000000L));
        // No match at all
        assertEquals(0, LongUtil.commonPrefixLength(0L, 0xFFFFFFFFFFFFFFFFL));
    }
}