package ch.hsr.geohash;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class WGS84PointPublicTest {

    @Test
    public void testConstructorAndGetters_public() {
        WGS84Point point = new WGS84Point(-35.4, 75.2);
        assertEquals(-35.4, point.getLatitude(), 0.0);
        assertEquals(75.2, point.getLongitude(), 0.0);
    }

    @Test
    public void testCopyConstructor_public() {
        WGS84Point orig = new WGS84Point(-60.5, 128.3);
        WGS84Point copy = new WGS84Point(orig);
        assertEquals(orig, copy);
        assertEquals(orig.hashCode(), copy.hashCode());
    }

    @Test
    public void testToString_public() {
        WGS84Point point = new WGS84Point(-13.2, 102.8);
        assertEquals("(-13.2,102.8)", point.toString());
    }

    @Test
    public void testEqualsAndHashCode_public() {
        WGS84Point p1 = new WGS84Point(-90, 180);
        WGS84Point p2 = new WGS84Point(-90, 180);
        WGS84Point p3 = new WGS84Point(89.9, -179.9);
        assertEquals(p1, p2);
        assertEquals(p1.hashCode(), p2.hashCode());
        assertNotEquals(p1, p3);
        assertNotEquals(p2, null);
        assertNotEquals(p3, "some string");
    }

    @Test
    public void testOutOfRangeLatitude_public() {
        assertThrows(IllegalArgumentException.class, () -> new WGS84Point(91.0, 10.0));
        assertThrows(IllegalArgumentException.class, () -> new WGS84Point(-91.0, 10.0));
    }

    @Test
    public void testOutOfRangeLongitude_public() {
        assertThrows(IllegalArgumentException.class, () -> new WGS84Point(0.0, 181.0));
        assertThrows(IllegalArgumentException.class, () -> new WGS84Point(0.0, -181.0));
    }
}