package ch.hsr.geohash.util;

import ch.hsr.geohash.BoundingBox;
import ch.hsr.geohash.WGS84Point;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class GeoHashSizeTableTest {
    @Test
    public void testNumberOfBitsForOverlappingGeoHashTypicalBox() {
        BoundingBox box = new BoundingBox(-1, 1, -1, 1);
        int bits = GeoHashSizeTable.numberOfBitsForOverlappingGeoHash(box);
        assertTrue(bits > 0 && bits <= 63);
    }

    @Test
    public void testNumberOfBitsForTinyBoxHighPrecision() {
        BoundingBox box = new BoundingBox(0, 0.0001, 0, 0.0001);
        int bits = GeoHashSizeTable.numberOfBitsForOverlappingGeoHash(box);
        assertTrue(bits <= 63 && bits > 0);
    }

    @Test
    public void testNumberOfBitsForHugeBoxLowPrecision() {
        BoundingBox box = new BoundingBox(-80, 80, -150, 150);
        int bits = GeoHashSizeTable.numberOfBitsForOverlappingGeoHash(box);
        assertTrue(bits < 63 && bits > 0);
    }
}