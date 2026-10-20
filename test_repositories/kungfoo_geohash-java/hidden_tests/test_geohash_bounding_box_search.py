import pytest

from src.geohash.bounding_box import BoundingBox
from src.geohash.geohash import GeoHash
from src.geohash.queries.bounding_box_query import GeoHashBoundingBoxQuery
from src.geohash.queries.geohash_query import GeoHashQuery

def test_several_bounding_boxes():
    def check_search_yields_correct_number_of_hashes(south_lat, north_lat, west_lon, east_lon):
        search = GeoHashBoundingBoxQuery(BoundingBox(south_lat, north_lat, west_lon, east_lon))
        size = len(search.get_search_hashes())
        assert 0 < size <= 8

    def check_search_yields_correct_hashes(south_lat, north_lat, west_lon, east_lon, *hashes):
        search = GeoHashBoundingBoxQuery(BoundingBox(south_lat, north_lat, west_lon, east_lon))
        found_hashes = search.get_search_hashes()
        assert len(found_hashes) == len(hashes)
        for expected in hashes:
            assert GeoHash.from_geohash_string(expected) in found_hashes

    def check_search_yields_correct_binary_hashes(south_lat, north_lat, west_lon, east_lon, *hashes):
        search = GeoHashBoundingBoxQuery(BoundingBox(south_lat, north_lat, west_lon, east_lon))
        found_hashes = search.get_search_hashes()
        assert len(found_hashes) == len(hashes)
        for expected in hashes:
            assert GeoHash.from_binary_string(expected) in found_hashes

    check_search_yields_correct_number_of_hashes(40.2090980098, 40.21982983232432, -22.523432424324, -22.494234232442)
    check_search_yields_correct_number_of_hashes(40.09872762, 41.23452234, 30.0113312322, 31.23432)

    check_search_yields_correct_hashes(47.3002, 47.447907, 8.471276, 8.760941, "u0qj")
    check_search_yields_correct_hashes(47.157502, 47.329727, 8.562244, 8.859215, "u0qj", "u0qm", "u0qh", "u0qk")

    check_search_yields_correct_number_of_hashes(40.2090980098, 40.21982983232432, 170.523432424324, -170.494234232442)
    check_search_yields_correct_number_of_hashes(40.2090980098, 40.21982983232432, 170.523432424324, 160.494234232442)

    check_search_yields_correct_hashes(40.2090980098, 40.21982983232432, 170.523432424324, -170.494234232442, "xz", "8p")
    check_search_yields_correct_binary_hashes(47.157502, 47.329727, 179.062244, -179.859215, "1111101010101111", "010100000000010100000", "010100000000010100010")

    # Check duplicate handling
    check_search_yields_correct_binary_hashes(47.157502, 47.329727, 179.062244, 160, "")
    check_search_yields_correct_binary_hashes(47.157502, 47.329727, 179.062244, -1, "01", "1111101010101111")