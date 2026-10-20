import pytest
from src.geohash.wgs84point import WGS84Point

def test_constructor_and_getters():
    point = WGS84Point(10.0, 20.0)
    assert point.get_latitude() == pytest.approx(10.0)
    assert point.get_longitude() == pytest.approx(20.0)

def test_copy_constructor():
    orig = WGS84Point(15.5, -30.2)
    copy = WGS84Point(orig)
    assert orig == copy
    assert hash(orig) == hash(copy)

def test_to_string():
    point = WGS84Point(10.0, -45.7)
    assert str(point) == "(10.0,-45.7)"

def test_equals_and_hash_code():
    p1 = WGS84Point(5, 6)
    p2 = WGS84Point(5, 6)
    p3 = WGS84Point(6, 5)
    assert p1 == p2
    assert hash(p1) == hash(p2)
    assert p1 != p3
    assert p2 != None
    assert p3 != "not a point"

def test_out_of_range_latitude():
    with pytest.raises(ValueError):
        WGS84Point(95.0, 20.0)
    with pytest.raises(ValueError):
        WGS84Point(-95.0, 20.0)

def test_out_of_range_longitude():
    with pytest.raises(ValueError):
        WGS84Point(10.0, 200.0)
    with pytest.raises(ValueError):
        WGS84Point(10.0, -200.0)