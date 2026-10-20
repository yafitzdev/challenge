import pytest
from src.geohash.wgs84point import WGS84Point

def test_constructor_and_getters_public():
    point = WGS84Point(-35.4, 75.2)
    assert point.get_latitude() == pytest.approx(-35.4)
    assert point.get_longitude() == pytest.approx(75.2)

def test_copy_constructor_public():
    orig = WGS84Point(-60.5, 128.3)
    copy = WGS84Point(orig)
    assert orig == copy
    assert hash(orig) == hash(copy)

def test_to_string_public():
    point = WGS84Point(-13.2, 102.8)
    assert str(point) == "(-13.2,102.8)"

def test_equals_and_hash_code_public():
    p1 = WGS84Point(-90, 180)
    p2 = WGS84Point(-90, 180)
    p3 = WGS84Point(89.9, -179.9)
    assert p1 == p2
    assert hash(p1) == hash(p2)
    assert p1 != p3
    assert p2 is not None
    assert p3 != "some string"

def test_out_of_range_latitude_public():
    with pytest.raises(ValueError):
        WGS84Point(91.0, 10.0)
    with pytest.raises(ValueError):
        WGS84Point(-91.0, 10.0)

def test_out_of_range_longitude_public():
    with pytest.raises(ValueError):
        WGS84Point(0.0, 181.0)
    with pytest.raises(ValueError):
        WGS84Point(0.0, -181.0)