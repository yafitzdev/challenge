from src.geohash.bounding_box import BoundingBox
from src.geohash.util.bounding_box_geohash_iterator import BoundingBoxGeoHashIterator
from src.geohash.util.two_geohash_bounding_box import TwoGeoHashBoundingBox
from src.geohash.geohash import GeoHash

def check_iterator(iter):
    new_box = iter.get_bounding_box().get_bounding_box()
    hashes = []
    prev = None
    while iter.has_next():
        gh = iter.next()
        hashes.append(gh)
        if prev is not None:
            assert prev < gh
        assert new_box.contains(gh.get_originating_point())
        prev = gh
    return hashes

def test_iter():
    box = BoundingBox(37.7, 37.84, -122.52, -122.35)
    iter = BoundingBoxGeoHashIterator(TwoGeoHashBoundingBox.with_bit_precision(box, 10))
    check_iterator(iter)

def test_iter2():
    box = BoundingBox(37.7, 37.84, -122.52, -122.35)
    iter = BoundingBoxGeoHashIterator(TwoGeoHashBoundingBox.with_bit_precision(box, 35))
    check_iterator(iter)

def test_iter3():
    box = BoundingBox(28.5, 67.15, -33.2, 44.5)
    iter = BoundingBoxGeoHashIterator(TwoGeoHashBoundingBox.with_character_precision(box, 2))
    hashes = check_iterator(iter)
    assert len(hashes) == 49

def test_endless_iterator():
    box = BoundingBox(72.28907, 88.62655, -50.976562, 170.50781)
    two_geo = TwoGeoHashBoundingBox.with_character_precision(box, 2)
    iterator = BoundingBoxGeoHashIterator(two_geo)

    hashes = set()
    while iterator.has_next():
        hash = iterator.next()
        assert hash not in hashes, f"Hash has already been produced: {hash}"
        hashes.add(hash)

def test_all_cells():
    box = BoundingBox(-90, 90, -180, 180)
    two_geo = TwoGeoHashBoundingBox.with_character_precision(box, 2)
    iterator = BoundingBoxGeoHashIterator(two_geo)

    hashes = set()
    while iterator.has_next():
        hash = iterator.next()
        hashes.add(hash)
    assert len(hashes) == 1024

def test_top_right_corner():
    box = BoundingBox(84.4, 84.9, 169.3, 179.6)
    two_geo = TwoGeoHashBoundingBox.with_character_precision(box, 2)
    iterator = BoundingBoxGeoHashIterator(two_geo)
    hashes = set()
    while iterator.has_next():
        hash = iterator.next()
        assert hash not in hashes
        hashes.add(hash)