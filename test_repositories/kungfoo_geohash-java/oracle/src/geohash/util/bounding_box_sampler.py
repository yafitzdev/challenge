from .._java import JavaRandom

INTEGER_MAX_VALUE = 2 ** 31 - 1


class BoundingBoxSampler:
    """Select random samples of geohashes within a bounding box, without replacement."""

    def __init__(self, bbox, seed=None):
        from ..geohash import GeoHash
        self._bounding_box = bbox
        self._already_used = set()
        max_samples_long = GeoHash.steps_between(bbox.get_south_west_corner(), bbox.get_north_east_corner())
        if max_samples_long > INTEGER_MAX_VALUE:
            raise ValueError("This bounding box is too big too sample using this algorithm")
        self._max_samples = int(max_samples_long)
        self._rand = JavaRandom(seed)

    def get_bounding_box(self):
        return self._bounding_box

    def next(self):
        """Return next sample, or None if all samples have been returned."""
        # Java implementation recurses when the sample lies outside the box; a loop is equivalent.
        while True:
            if len(self._already_used) == self._max_samples:
                return None
            idx = self._rand.next_int(self._max_samples + 1)
            while idx in self._already_used:
                idx = self._rand.next_int(self._max_samples + 1)
            self._already_used.add(idx)
            gh = self._bounding_box.get_south_west_corner().next(idx)
            if self._bounding_box.get_bounding_box().contains(gh.get_originating_point()):
                return gh
