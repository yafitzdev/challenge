from src.geohash.bounding_box import BoundingBox
from src.geohash.util.bounding_box_geohash_iterator import BoundingBoxGeoHashIterator

def test_iterate_bounding_box_public():
    box = BoundingBox(10, 12, 33, 35)
    it = BoundingBoxGeoHashIterator(box, 6)

    hashes = []
    while it.has_next():
        hashes.append(it.next().to_base32())
    assert hashes
    for hashstr in hashes:
        assert len(hashstr) == 6
    assert len(hashes) == len(set(hashes))

def test_single_cell_bounding_box_public():
    very_small_box = BoundingBox(0.01, 0.015, -0.02, -0.015)
    it = BoundingBoxGeoHashIterator(very_small_box, 5)

    hashes = []
    while it.has_next():
        hashes.append(it.next().to_base32())
    assert len(hashes) == 1