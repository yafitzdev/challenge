import pytest

from src.geohash.wgs84point import WGS84Point
from src.geohash.queries.circle_query import GeoHashCircleQuery

def test_issue3_with_circle_query():
    center = WGS84Point(39.86391280373075, 116.37356590048701)
    query = GeoHashCircleQuery(center, 589)

    test1 = WGS84Point(39.8648866576058, 116.378465869303)   # ~430m
    test2 = WGS84Point(39.8664787092599, 116.378552856158)   # ~510m
    test3 = WGS84Point(39.8786787092599, 116.378552856158)   # ~600m

    assert query.contains(test1)
    assert query.contains(test2)
    assert not query.contains(test3)

def test_180_meridian_circle_query():
    center = WGS84Point(39.86391280373075, 179.98356590048701)
    query = GeoHashCircleQuery(center, 3000)

    test1 = WGS84Point(39.8648866576058, 180)
    test2 = WGS84Point(39.8664787092599, -180)
    test3 = WGS84Point(39.8686787092599, -179.9957861565146)
    test4 = WGS84Point(39.8686787092599, 179.0057861565146)
    test5 = WGS84Point(39.8686787092599, -179.0)

    assert query.contains(test1)
    assert query.contains(test2)
    assert query.contains(test3)
    assert not query.contains(test4)
    assert not query.contains(test5)