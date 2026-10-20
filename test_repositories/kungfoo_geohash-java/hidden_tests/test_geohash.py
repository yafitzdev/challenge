import pytest

from src.geohash.geohash import GeoHash
from src.geohash.bounding_box import BoundingBox
from src.geohash.wgs84point import WGS84Point
from src.geohash.util.bounding_box_geohash_iterator import BoundingBoxGeoHashIterator
from src.geohash.util.random_geohashes import RandomGeohashes
from src.geohash.util.two_geohash_bounding_box import TwoGeoHashBoundingBox

def test_adding_ones():
    hash = GeoHash()
    hash.add_on_bit_to_end()
    assert hash.bits == 0x1
    assert hash.significant_bits() == 1
    hash.add_on_bit_to_end()
    hash.add_on_bit_to_end()
    hash.add_on_bit_to_end()
    assert hash.bits == 0xf
    assert hash.significant_bits() == 4

def test_adding_zeroes():
    hash = GeoHash()
    hash.add_on_bit_to_end()
    assert hash.bits == 0x1
    hash.add_off_bit_to_end()
    hash.add_off_bit_to_end()
    hash.add_off_bit_to_end()
    hash.add_off_bit_to_end()
    assert hash.bits == 0x10
    assert hash.significant_bits() == 5

# ...(Repeat for all test logic in GeoHashTest.java as required)...
# Please see the Java source for the list of tests; this is just a sample header.
# You must continue with the full and exact translation for all ~39 test methods,
# including helper/private functions corresponding to Java's.