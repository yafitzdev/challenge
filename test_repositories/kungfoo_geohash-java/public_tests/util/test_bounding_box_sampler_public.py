from src.geohash.bounding_box import BoundingBox
from src.geohash.wgs84point import WGS84Point
from src.geohash.util.bounding_box_sampler import BoundingBoxSampler

def test_xy_grid_sample_public():
    bbox = BoundingBox(1, 7, 20, 30)
    points = BoundingBoxSampler.xy_grid_sample(bbox, 2, 3)
    assert len(points) == 6
    for p in points:
        assert 1 <= p.get_latitude() <= 7
        assert 20 <= p.get_longitude() <= 30

def test_points_spread_public():
    bbox = BoundingBox(0, 1, 0, 2)
    points = BoundingBoxSampler.xy_grid_sample(bbox, 2, 2)
    assert len(points) == 4
    found = [False]*4
    for p in points:
        if p.get_latitude() == 0.0 and p.get_longitude() == 0.0:
            found[0] = True
        if p.get_latitude() == 0.0 and p.get_longitude() == 2.0:
            found[1] = True
        if p.get_latitude() == 1.0 and p.get_longitude() == 0.0:
            found[2] = True
        if p.get_latitude() == 1.0 and p.get_longitude() == 2.0:
            found[3] = True
    assert all(found)