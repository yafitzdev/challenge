package ch.hsr.geohash.util;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class LongUtilPublicTest {
    @Test
    public void testCommonPrefixLength_public() {
        // Same value, all 1s
        assertEquals(64, LongUtil.commonPrefixLength(0xFFFFFFFFFFFFFFFFL, 0xFFFFFFFFFFFFFFFFL));
        // Differs at 2nd bit
        assertEquals(1, LongUtil.commonPrefixLength(0x4000000000000000L, 0xC000000000000000L));
        // Differs at 32nd bit
        assertEquals(31, LongUtil.commonPrefixLength(0x80000000FFFFFFFFL, 0x800000007FFFFFFFL));
    }
}