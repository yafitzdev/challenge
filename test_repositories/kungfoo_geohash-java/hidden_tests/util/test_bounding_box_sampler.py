from src.geohash.bounding_box import BoundingBox
from src.geohash.util.bounding_box_sampler import BoundingBoxSampler
from src.geohash.util.two_geohash_bounding_box import TwoGeoHashBoundingBox

def test_sampler():
    bbox = BoundingBox(37.7, 37.84, -122.52, -122.35)
    sampler = BoundingBoxSampler(TwoGeoHashBoundingBox.with_bit_precision(bbox, 35), 1179)
    bbox = sampler.get_bounding_box().get_bounding_box()
    gh = sampler.next()
    hashes = set()
    sum_of_comp = 0
    crossing_zero = 0
    prev = None
    while gh is not None:
        assert bbox.contains(gh.get_originating_point())
        assert gh.to_base32() not in hashes
        hashes.add(gh.to_base32())
        if prev is not None:
            sum_of_comp += prev.compare_to(gh)
        prev = gh
        if sum_of_comp == 0:
            crossing_zero += 1
        gh = sampler.next()
    assert len(hashes) == 12875
    assert abs(sum_of_comp + 40) <= 80  # Allow for float fuzz
    assert crossing_zero == 123