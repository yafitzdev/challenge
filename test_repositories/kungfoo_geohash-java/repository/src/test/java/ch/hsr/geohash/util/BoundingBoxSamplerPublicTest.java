package ch.hsr.geohash.util;

import ch.hsr.geohash.BoundingBox;
import ch.hsr.geohash.WGS84Point;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class BoundingBoxSamplerPublicTest {

    @Test
    public void testXYGridSample_public() {
        // Use different bbox and xy than prod test
        BoundingBox bbox = new BoundingBox(1, 7, 20, 30);
        List<WGS84Point> points = BoundingBoxSampler.xyGridSample(bbox, 2, 3);
        assertEquals(2 * 3, points.size());
        // All points should be within bbox
        for (WGS84Point p : points) {
            assertTrue(p.getLatitude() >= 1 && p.getLatitude() <= 7, "Latitude inside bbox");
            assertTrue(p.getLongitude() >= 20 && p.getLongitude() <= 30, "Longitude inside bbox");
        }
    }

    @Test
    public void testPointsSpread_public() {
        BoundingBox bbox = new BoundingBox(0, 1, 0, 2);
        List<WGS84Point> points = BoundingBoxSampler.xyGridSample(bbox, 2, 2);
        assertEquals(4, points.size());
        // Points should cover corners
        boolean[] found = new boolean[4];
        for (WGS84Point p : points) {
            if (p.getLatitude() == 0.0 && p.getLongitude() == 0.0) found[0] = true;
            if (p.getLatitude() == 0.0 && p.getLongitude() == 2.0) found[1] = true;
            if (p.getLatitude() == 1.0 && p.getLongitude() == 0.0) found[2] = true;
            if (p.getLatitude() == 1.0 && p.getLongitude() == 2.0) found[3] = true;
        }
        for (boolean f : found) assertTrue(f);
    }
}