package ch.hsr.geohash.util;

import ch.hsr.geohash.BoundingBox;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class BoundingBoxGeoHashIteratorPublicTest {

    @Test
    public void testIterateBoundingBox_public() {
        // Slightly different bounding box than production test
        BoundingBox box = new BoundingBox(10, 12, 33, 35);
        BoundingBoxGeoHashIterator it = new BoundingBoxGeoHashIterator(box, 6);

        List<String> hashes = new ArrayList<>();
        while (it.hasNext()) {
            hashes.add(it.next().toBase32());
        }
        assertFalse(hashes.isEmpty());
        // Check that all hash strings are of length 6
        for (String hash : hashes) {
            assertEquals(6, hash.length());
        }
        // hashes returned should be unique
        assertEquals(hashes.size(), hashes.stream().distinct().count());
    }

    @Test
    public void testSingleCellBoundingBox_public() {
        // A bounding box smaller than geohash cell, should result in one hash
        BoundingBox verySmallBox = new BoundingBox(0.01, 0.015, -0.02, -0.015);
        BoundingBoxGeoHashIterator it = new BoundingBoxGeoHashIterator(verySmallBox, 5);

        List<String> hashes = new ArrayList<>();
        while (it.hasNext()) {
            hashes.add(it.next().toBase32());
        }
        assertEquals(1, hashes.size());
    }
}