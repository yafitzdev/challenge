from ..bounding_box import BoundingBox
from ..util.vincenty_geodesy import VincentyGeodesy
from .._java import java_double_to_string
from .bounding_box_query import GeoHashBoundingBoxQuery
from .geohash_query import GeoHashQuery


class GeoHashCircleQuery(GeoHashQuery):
    def __init__(self, center, radius):
        self._radius = float(radius)
        self._center = center
        ne = VincentyGeodesy.move_in_direction(VincentyGeodesy.move_in_direction(center, 0, radius), 90, radius)
        sw = VincentyGeodesy.move_in_direction(VincentyGeodesy.move_in_direction(center, 180, radius), 270, radius)
        self._query = GeoHashBoundingBoxQuery(BoundingBox(sw, ne))

    def contains(self, obj):
        return self._query.contains(obj)

    def get_wkt_box(self):
        return self._query.get_wkt_box()

    def get_search_hashes(self):
        return self._query.get_search_hashes()

    def __str__(self):
        return "Cicle Query [center=" + str(self._center) + ", radius=" + self._get_radius_string() + "]"

    def _get_radius_string(self):
        if self._radius > 1000:
            return java_double_to_string(self._radius / 1000) + "km"
        return java_double_to_string(self._radius) + "m"
