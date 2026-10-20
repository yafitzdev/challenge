from src.geohash.bounding_box import BoundingBox
from src.geohash.util.geohash_size_table import GeoHashSizeTable

def test_number_of_bits_for_overlapping_geohash_typical_box():
    box = BoundingBox(-1, 1, -1, 1)
    bits = GeoHashSizeTable.number_of_bits_for_overlapping_geohash(box)
    assert bits > 0 and bits <= 63

def test_number_of_bits_for_tiny_box_high_precision():
    box = BoundingBox(0, 0.0001, 0, 0.0001)
    bits = GeoHashSizeTable.number_of_bits_for_overlapping_geohash(box)
    assert bits <= 63 and bits > 0

def test_number_of_bits_for_huge_box_low_precision():
    box = BoundingBox(-80, 80, -150, 150)
    bits = GeoHashSizeTable.number_of_bits_for_overlapping_geohash(box)
    assert bits < 63 and bits > 0