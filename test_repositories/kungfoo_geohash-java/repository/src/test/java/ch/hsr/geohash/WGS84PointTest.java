package ch.hsr.geohash;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class WGS84PointTest {

    @Test
    public void testConstructorAndGetters() {
        WGS84Point point = new WGS84Point(10.0, 20.0);
        assertEquals(10.0, point.getLatitude(), 0.0);
        assertEquals(20.0, point.getLongitude(), 0.0);
    }

    @Test
    public void testCopyConstructor() {
        WGS84Point orig = new WGS84Point(15.5, -30.2);
        WGS84Point copy = new WGS84Point(orig);
        assertEquals(orig, copy);
        assertEquals(orig.hashCode(), copy.hashCode());
    }

    @Test
    public void testToString() {
        WGS84Point point = new WGS84Point(10.0, -45.7);
        assertEquals("(10.0,-45.7)", point.toString());
    }

    @Test
    public void testEqualsAndHashCode() {
        WGS84Point p1 = new WGS84Point(5, 6);
        WGS84Point p2 = new WGS84Point(5, 6);
        WGS84Point p3 = new WGS84Point(6, 5);
        assertEquals(p1, p2);
        assertEquals(p1.hashCode(), p2.hashCode());
        assertNotEquals(p1, p3);
        assertNotEquals(p2, null);
        assertNotEquals(p3, "not a point");
    }

    @Test
    public void testOutOfRangeLatitude() {
        assertThrows(IllegalArgumentException.class, () -> new WGS84Point(95.0, 20.0));
        assertThrows(IllegalArgumentException.class, () -> new WGS84Point(-95.0, 20.0));
    }

    @Test
    public void testOutOfRangeLongitude() {
        assertThrows(IllegalArgumentException.class, () -> new WGS84Point(10.0, 200.0));
        assertThrows(IllegalArgumentException.class, () -> new WGS84Point(10.0, -200.0));
    }
}