package ch.hsr.geohash.util;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class GeoHashSizeTablePublicTest {

    @Test
    public void testWidthHeight_public() {
        assertEquals(125.0, GeoHashSizeTable.widthDegreesForPrecision(1), 0.001);
        assertEquals(5.0, GeoHashSizeTable.widthDegreesForPrecision(3), 0.001);
        assertEquals(0.019, GeoHashSizeTable.widthDegreesForPrecision(7), 0.001);
        assertEquals(625.0, GeoHashSizeTable.heightDegreesForPrecision(1), 0.001);
        assertEquals(0.019, GeoHashSizeTable.heightDegreesForPrecision(7), 0.001);
    }

    @Test
    public void testMaxPrecisionAndZero_public() {
        assertEquals(0.0006, GeoHashSizeTable.widthDegreesForPrecision(12), 0.0001);
        assertEquals(0.0006, GeoHashSizeTable.heightDegreesForPrecision(12), 0.0001);
        // At precision 0, returned width/height should cover whole world
        assertEquals(360.0, GeoHashSizeTable.widthDegreesForPrecision(0), 0.001);
        assertEquals(180.0, GeoHashSizeTable.heightDegreesForPrecision(0), 0.001);
    }
}