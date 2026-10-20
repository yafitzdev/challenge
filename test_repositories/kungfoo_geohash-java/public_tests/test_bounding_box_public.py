import pytest
from src.geohash.bounding_box import BoundingBox
from src.geohash.wgs84point import WGS84Point

def test_bounding_box_construct_corners_public():
    sw = WGS84Point(-55, 110)
    ne = WGS84Point(-15, 150)
    box = BoundingBox(sw, ne)
    assert box.get_south_west_corner().get_latitude() == pytest.approx(-55)
    assert box.get_south_west_corner().get_longitude() == pytest.approx(110)
    assert box.get_north_east_corner().get_latitude() == pytest.approx(-15)
    assert box.get_north_east_corner().get_longitude() == pytest.approx(150)
    assert box.get_south_latitude() == pytest.approx(-55)
    assert box.get_north_latitude() == pytest.approx(-15)
    assert box.get_west_longitude() == pytest.approx(110)
    assert box.get_east_longitude() == pytest.approx(150)

def test_latitude_longitude_size_public():
    box = BoundingBox(22, 44, -45, -33)
    assert box.get_latitude_size() == pytest.approx(22.0)
    assert box.get_longitude_size() == pytest.approx(12.0)

def test_longitude_wrap_around_meridian_public():
    box = BoundingBox(-40, 40, 179, -179)
    assert box.get_longitude_size() > 0

def test_longitude_edge_case_full_globe_public():
    box = BoundingBox(0, 90, -180, 180)
    assert box.get_longitude_size() == pytest.approx(360.0, abs=0.00001)

def test_equals_and_hash_code_public():
    b1 = BoundingBox(-10, 10, 50, 100)
    b2 = BoundingBox(-10, 10, 50, 100)
    b3 = BoundingBox(-11, 10, 50, 100)
    assert b1 == b2
    assert hash(b1) == hash(b2)
    assert b1 != b3
    assert b1 is not None
    assert b1 != "something else"

def test_throws_on_south_greater_than_north_public():
    with pytest.raises(ValueError):
        BoundingBox(20, 10, 0, 0)

def test_throws_on_out_of_range_public():
    with pytest.raises(ValueError):
        BoundingBox(-100, 10, 0, 0)
    with pytest.raises(ValueError):
        BoundingBox(-10, 95.5, 0, 0)
    with pytest.raises(ValueError):
        BoundingBox(-10, 10, 0, 200)
    with pytest.raises(ValueError):
        BoundingBox(-10, 10, -200, 0)