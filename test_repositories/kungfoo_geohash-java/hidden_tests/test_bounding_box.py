import pytest
from src.geohash.bounding_box import BoundingBox
from src.geohash.wgs84point import WGS84Point

def test_bounding_box_construct_corners():
    sw = WGS84Point(-10, -20)
    ne = WGS84Point(10, 20)
    box = BoundingBox(sw, ne)
    assert box.get_south_west_corner().get_latitude() == pytest.approx(-10)
    assert box.get_south_west_corner().get_longitude() == pytest.approx(-20)
    assert box.get_north_east_corner().get_latitude() == pytest.approx(10)
    assert box.get_north_east_corner().get_longitude() == pytest.approx(20)
    assert box.get_south_latitude() == pytest.approx(-10)
    assert box.get_north_latitude() == pytest.approx(10)
    assert box.get_west_longitude() == pytest.approx(-20)
    assert box.get_east_longitude() == pytest.approx(20)

def test_latitude_longitude_size():
    box = BoundingBox(-10, 10, -20, 20)
    assert box.get_latitude_size() == pytest.approx(20)
    assert box.get_longitude_size() == pytest.approx(40)

def test_longitude_wrap_around_meridian():
    # east < west means crossing meridian
    box = BoundingBox(-10, 10, 170, -170)
    assert box.get_longitude_size() > 0

def test_longitude_edge_case_full_globe():
    box = BoundingBox(-10, 10, -180, 180)
    assert box.get_longitude_size() == pytest.approx(360.0, abs=0.00001)

def test_equals_and_hash_code():
    box1 = BoundingBox(0, 10, 0, 20)
    box2 = BoundingBox(0, 10, 0, 20)
    box3 = BoundingBox(1, 10, 0, 20)
    assert box1 == box2
    assert hash(box1) == hash(box2)
    assert box1 != box3
    assert box1 != None
    assert box1 != "not a box"

def test_throws_on_south_greater_than_north():
    with pytest.raises(ValueError):
        BoundingBox(10, -10, 0, 0)

def test_throws_on_out_of_range():
    with pytest.raises(ValueError):
        BoundingBox(-100, 10, 0, 0)
    with pytest.raises(ValueError):
        BoundingBox(-10, 95, 0, 0)
    with pytest.raises(ValueError):
        BoundingBox(-10, 10, 0, 190)
    with pytest.raises(ValueError):
        BoundingBox(-10, 10, -190, 0)