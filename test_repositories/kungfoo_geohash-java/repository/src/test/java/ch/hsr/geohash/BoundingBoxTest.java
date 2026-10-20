package ch.hsr.geohash;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BoundingBoxTest {

    @Test
    public void testBoundingBoxConstructCorners() {
        WGS84Point sw = new WGS84Point(-10, -20);
        WGS84Point ne = new WGS84Point(10, 20);
        BoundingBox box = new BoundingBox(sw, ne);
        assertEquals(-10, box.getSouthWestCorner().getLatitude(), 0.0);
        assertEquals(-20, box.getSouthWestCorner().getLongitude(), 0.0);
        assertEquals(10, box.getNorthEastCorner().getLatitude(), 0.0);
        assertEquals(20, box.getNorthEastCorner().getLongitude(), 0.0);
        assertEquals(-10, box.getSouthLatitude(), 0.0);
        assertEquals(10, box.getNorthLatitude(), 0.0);
        assertEquals(-20, box.getWestLongitude(), 0.0);
        assertEquals(20, box.getEastLongitude(), 0.0);
    }

    @Test
    public void testLatitudeLongitudeSize() {
        BoundingBox box = new BoundingBox(-10, 10, -20, 20);
        assertEquals(20, box.getLatitudeSize(), 0.0);
        assertEquals(40, box.getLongitudeSize(), 0.0);
    }

    @Test
    public void testLongitudeWrapAroundMeridian() {
        // east < west means crossing meridian
        BoundingBox box = new BoundingBox(-10, 10, 170, -170);
        assertTrue(box.getLongitudeSize() > 0);
    }

    @Test
    public void testLongitudeEdgeCaseFullGlobe() {
        BoundingBox box = new BoundingBox(-10, 10, -180, 180);
        assertEquals(360.0, box.getLongitudeSize(), 0.00001);
    }

    @Test
    public void testEqualsAndHashCode() {
        BoundingBox box1 = new BoundingBox(0, 10, 0, 20);
        BoundingBox box2 = new BoundingBox(0, 10, 0, 20);
        BoundingBox box3 = new BoundingBox(1, 10, 0, 20);
        assertEquals(box1, box2);
        assertEquals(box1.hashCode(), box2.hashCode());
        assertNotEquals(box1, box3);
        assertNotEquals(box1, null);
        assertNotEquals(box1, "not a box");
    }

    @Test
    public void testThrowsOnSouthGreaterThanNorth() {
        assertThrows(IllegalArgumentException.class, () -> new BoundingBox(10, -10, 0, 0));
    }

    @Test
    public void testThrowsOnOutOfRange() {
        assertThrows(IllegalArgumentException.class, () -> new BoundingBox(-100, 10, 0, 0));
        assertThrows(IllegalArgumentException.class, () -> new BoundingBox(-10, 95, 0, 0));
        assertThrows(IllegalArgumentException.class, () -> new BoundingBox(-10, 10, 0, 190));
        assertThrows(IllegalArgumentException.class, () -> new BoundingBox(-10, 10, -190, 0));
    }
}