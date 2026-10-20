from ..bounding_box import BoundingBox
from ..geohash import GeoHash
from ..wgs84point import WGS84Point
from ..util.geohash_size_table import GeoHashSizeTable
from .._java import shl, java_double_to_string as _ds
from .geohash_query import GeoHashQuery


class GeoHashBoundingBoxQuery(GeoHashQuery):
    def __init__(self, bbox):
        self._search_hashes = []
        self._bounding_box = None
        if not bbox.intersects180_meridian():
            self._generate_search_hashes(bbox)
        else:
            east_box = BoundingBox(bbox.get_south_latitude(), bbox.get_north_latitude(), bbox.get_west_longitude(), 180)
            west_box = BoundingBox(bbox.get_south_latitude(), bbox.get_north_latitude(), -180, bbox.get_east_longitude())
            self._generate_search_hashes(east_box)
            self._generate_search_hashes(west_box)

        for h in self._search_hashes:
            if self._bounding_box is None:
                self._bounding_box = BoundingBox(h.get_bounding_box())
            else:
                self._bounding_box.expand_to_include(h.get_bounding_box())

        for h in self._search_hashes:
            if h.significant_bits() == 0:
                self._search_hashes.clear()
                self._search_hashes.append(h)
                return

        F = GeoHash.FIRST_BIT_FLAGGED
        to_remove = []
        for h in self._search_hashes:
            for cmp in self._search_hashes:
                if cmp.significant_bits() < h.significant_bits():
                    hash_copy = h.long_value()
                    cmp_copy = cmp.long_value()
                    equal_bits = 0
                    # Java loops forever if all 64 bits agree; bounded here (only reachable in that degenerate case)
                    while (cmp_copy & F) == (hash_copy & F) and equal_bits < 64:
                        cmp_copy = shl(cmp_copy, 1)
                        hash_copy = shl(hash_copy, 1)
                        equal_bits += 1
                    if equal_bits == cmp.significant_bits():
                        to_remove.append(h)
                        break
        for h in to_remove:
            self._search_hashes.remove(h)

    def _generate_search_hashes(self, bbox):
        fitting_bits = GeoHashSizeTable.number_of_bits_for_overlapping_geohash(bbox)
        center = bbox.get_center()
        center_hash = GeoHash.with_bit_precision(center.get_latitude(), center.get_longitude(), fitting_bits)
        if self._hash_contains_bounding_box(center_hash, bbox):
            self._search_hashes.append(center_hash)
        else:
            self._expand_search(center_hash, bbox)

    def _expand_search(self, center_hash, bbox):
        self._search_hashes.append(center_hash)
        for adjacent in center_hash.get_adjacent():
            adjacent_box = adjacent.get_bounding_box()
            if adjacent_box.intersects(bbox) and adjacent not in self._search_hashes:
                self._search_hashes.append(adjacent)

    @staticmethod
    def _hash_contains_bounding_box(h, bbox):
        return h.contains(bbox.get_north_west_corner()) and h.contains(bbox.get_south_east_corner())

    def contains(self, obj):
        if isinstance(obj, WGS84Point):
            return self.contains(GeoHash.with_bit_precision(obj.get_latitude(), obj.get_longitude(), 64))
        for search_hash in self._search_hashes:
            if obj.within(search_hash):
                return True
        return False

    def get_search_hashes(self):
        return self._search_hashes

    def __str__(self):
        return "".join(str(h) + "\n" for h in self._search_hashes)

    def get_wkt_box(self):
        b = self._bounding_box
        return ("BOX(" + _ds(b.get_west_longitude()) + " " + _ds(b.get_south_latitude()) + ","
                + _ds(b.get_east_longitude()) + " " + _ds(b.get_north_latitude()) + ")")
