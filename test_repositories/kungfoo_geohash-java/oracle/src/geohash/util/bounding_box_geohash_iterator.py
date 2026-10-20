class BoundingBoxGeoHashIterator:
    """Iterate over all of the values within a bounding box at a particular resolution."""

    def __init__(self, bbox):
        self._bounding_box = bbox
        self._current = bbox.get_south_west_corner()

    def get_bounding_box(self):
        return self._bounding_box

    def has_next(self):
        return self._current is not None

    def next(self):
        if not self.has_next():
            raise StopIteration()
        rv = self._current
        if rv == self._bounding_box.get_north_east_corner():
            self._current = None
        else:
            self._current = rv.next()
            box = self._bounding_box.get_bounding_box()
            while self.has_next() and not box.contains(self._current.get_originating_point()):
                self._current = self._current.next()
        return rv

    __next__ = next

    def __iter__(self):
        return self

    def remove(self):
        raise NotImplementedError()
