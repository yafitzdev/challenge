package ch.hsr.geohash;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BoundingBoxPublicTest {

    @Test
    public void testBoundingBoxConstructCorners_public() {
        WGS84Point sw = new WGS84Point(-55, 110);
        WGS84Point ne = new WGS84Point(-15, 150);
        BoundingBox box = new BoundingBox(sw, ne);
        assertEquals(-55, box.getSouthWestCorner().getLatitude(), 0.0);
        assertEquals(110, box.getSouthWestCorner().getLongitude(), 0.0);
        assertEquals(-15, box.getNorthEastCorner().getLatitude(), 0.0);
        assertEquals(150, box.getNorthEastCorner().getLongitude(), 0.0);
        assertEquals(-55, box.getSouthLatitude(), 0.0);
        assertEquals(-15, box.getNorthLatitude(), 0.0);
        assertEquals(110, box.getWestLongitude(), 0.0);
        assertEquals(150, box.getEastLongitude(), 0.0);
    }

    @Test
    public void testLatitudeLongitudeSize_public() {
        BoundingBox box = new BoundingBox(22, 44, -45, -33);
        assertEquals(22.0, box.getLatitudeSize(), 0.0);
        assertEquals(12.0, box.getLongitudeSize(), 0.0);
    }

    @Test
    public void testLongitudeWrapAroundMeridian_public() {
        BoundingBox box = new BoundingBox(-40, 40, 179, -179);
        assertTrue(box.getLongitudeSize() > 0);
    }

    @Test
    public void testLongitudeEdgeCaseFullGlobe_public() {
        BoundingBox box = new BoundingBox(0, 90, -180, 180);
        assertEquals(360.0, box.getLongitudeSize(), 0.00001);
    }

    @Test
    public void testEqualsAndHashCode_public() {
        BoundingBox b1 = new BoundingBox(-10, 10, 50, 100);
        BoundingBox b2 = new BoundingBox(-10, 10, 50, 100);
        BoundingBox b3 = new BoundingBox(-11, 10, 50, 100);
        assertEquals(b1, b2);
        assertEquals(b1.hashCode(), b2.hashCode());
        assertNotEquals(b1, b3);
        assertNotEquals(b1, null);
        assertNotEquals(b1, "something else");
    }

    @Test
    public void testThrowsOnSouthGreaterThanNorth_public() {
        assertThrows(IllegalArgumentException.class, () -> new BoundingBox(20, 10, 0, 0));
    }

    @Test
    public void testThrowsOnOutOfRange_public() {
        assertThrows(IllegalArgumentException.class, () -> new BoundingBox(-100, 10, 0, 0));
        assertThrows(IllegalArgumentException.class, () -> new BoundingBox(-10, 95.5, 0, 0));
        assertThrows(IllegalArgumentException.class, () -> new BoundingBox(-10, 10, 0, 200));
        assertThrows(IllegalArgumentException.class, () -> new BoundingBox(-10, 10, -200, 0));
    }
}