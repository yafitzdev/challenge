from .wgs84point import WGS84Point
from .util.double_util import DoubleUtil
from ._java import double_hash, to_int


class BoundingBox:
    def __init__(self, *args):
        if len(args) == 2:
            sw, ne = args
            args = (sw.get_latitude(), ne.get_latitude(), sw.get_longitude(), ne.get_longitude())
        elif len(args) == 1:
            that = args[0]
            args = (that._south_latitude, that._north_latitude, that._west_longitude, that._east_longitude)
        if len(args) != 4:
            raise TypeError("BoundingBox expects 1, 2 or 4 arguments")
        south_latitude, north_latitude, west_longitude, east_longitude = (float(a) for a in args)
        if south_latitude > north_latitude:
            raise ValueError("The southLatitude must not be greater than the northLatitude")
        if (abs(south_latitude) > 90 or abs(north_latitude) > 90
                or abs(west_longitude) > 180 or abs(east_longitude) > 180):
            raise ValueError("The supplied coordinates are out of range.")
        self._north_latitude = north_latitude
        self._west_longitude = west_longitude
        self._south_latitude = south_latitude
        self._east_longitude = east_longitude
        self._intersects180_meridian = east_longitude < west_longitude

    def get_north_west_corner(self):
        return WGS84Point(self._north_latitude, self._west_longitude)

    def get_north_east_corner(self):
        return WGS84Point(self._north_latitude, self._east_longitude)

    def get_south_east_corner(self):
        return WGS84Point(self._south_latitude, self._east_longitude)

    def get_south_west_corner(self):
        return WGS84Point(self._south_latitude, self._west_longitude)

    def get_latitude_size(self):
        return self._north_latitude - self._south_latitude

    def get_longitude_size(self):
        if self._east_longitude == 180.0 and self._west_longitude == -180.0:
            return 360.0
        return DoubleUtil.remainder_with_fix(self._east_longitude - self._west_longitude, 360)

    def __eq__(self, obj):
        if self is obj:
            return True
        if isinstance(obj, BoundingBox):
            return (self._south_latitude == obj._south_latitude and self._west_longitude == obj._west_longitude
                    and self._north_latitude == obj._north_latitude and self._east_longitude == obj._east_longitude)
        return False

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        result = 17
        result = to_int(37 * result + double_hash(self._south_latitude))
        result = to_int(37 * result + double_hash(self._north_latitude))
        result = to_int(37 * result + double_hash(self._west_longitude))
        result = to_int(37 * result + double_hash(self._east_longitude))
        return result

    hash_code = __hash__

    def contains(self, point):
        return self._contains_latitude(point.get_latitude()) and self._contains_longitude(point.get_longitude())

    def intersects(self, other):
        if other._south_latitude > self._north_latitude or other._north_latitude < self._south_latitude:
            return False
        if not self._intersects180_meridian and not other._intersects180_meridian:
            return not (other._east_longitude < self._west_longitude or other._west_longitude > self._east_longitude)
        elif self._intersects180_meridian and not other._intersects180_meridian:
            return not (self._east_longitude < other._west_longitude and self._west_longitude > other._east_longitude)
        elif not self._intersects180_meridian and other._intersects180_meridian:
            return not (self._west_longitude > other._east_longitude and self._east_longitude < other._west_longitude)
        return True

    def __str__(self):
        return str(self.get_north_west_corner()) + " -> " + str(self.get_south_east_corner())

    __repr__ = __str__

    def get_center(self):
        center_latitude = (self._south_latitude + self._north_latitude) / 2
        center_longitude = (self._west_longitude + self._east_longitude) / 2
        if center_longitude > 180:
            center_longitude -= 360
        return WGS84Point(center_latitude, center_longitude)

    def expand_to_include(self, other):
        if isinstance(other, WGS84Point):
            self._expand_to_include_point(other)
        else:
            self._expand_to_include_box(other)

    def _expand_to_include_point(self, point):
        if point.get_latitude() < self._south_latitude:
            self._south_latitude = point.get_latitude()
        elif point.get_latitude() > self._north_latitude:
            self._north_latitude = point.get_latitude()
        if self._contains_longitude(point.get_longitude()):
            return
        distance_east_to_point = DoubleUtil.remainder_with_fix(point.get_longitude() - self._east_longitude, 360)
        distance_point_to_west = DoubleUtil.remainder_with_fix(self._west_longitude - point.get_longitude(), 360)
        if distance_east_to_point <= distance_point_to_west:
            self._east_longitude = point.get_longitude()
        else:
            self._west_longitude = point.get_longitude()
        self._intersects180_meridian = self._east_longitude < self._west_longitude

    def _expand_to_include_box(self, other):
        if other._south_latitude < self._south_latitude:
            self._south_latitude = other._south_latitude
        if other._north_latitude > self._north_latitude:
            self._north_latitude = other._north_latitude
        this_contains_other = (self._contains_longitude(other._east_longitude)
                               and self._contains_longitude(other._west_longitude))
        other_contains_this = (other._contains_longitude(self._east_longitude)
                               and other._contains_longitude(self._west_longitude))
        if this_contains_other and other_contains_this:
            self._east_longitude = 180.0
            self._west_longitude = -180.0
            self._intersects180_meridian = False
            return
        if this_contains_other:
            return
        if other_contains_this:
            self._east_longitude = other._east_longitude
            self._west_longitude = other._west_longitude
            self._intersects180_meridian = self._east_longitude < self._west_longitude
            return
        d_east = DoubleUtil.remainder_with_fix(other._east_longitude - self._east_longitude, 360)
        d_west = DoubleUtil.remainder_with_fix(self._west_longitude - other._west_longitude, 360)
        if d_east <= d_west:
            self._east_longitude = other._east_longitude
        else:
            self._west_longitude = other._west_longitude
        self._intersects180_meridian = self._east_longitude < self._west_longitude

    def _contains_latitude(self, latitude):
        return self._south_latitude <= latitude <= self._north_latitude

    def _contains_longitude(self, longitude):
        if self._intersects180_meridian:
            return longitude <= self._east_longitude or longitude >= self._west_longitude
        return self._west_longitude <= longitude <= self._east_longitude

    def get_east_longitude(self):
        return self._east_longitude

    def get_west_longitude(self):
        return self._west_longitude

    def get_north_latitude(self):
        return self._north_latitude

    def get_south_latitude(self):
        return self._south_latitude

    def intersects180_meridian(self):
        return self._intersects180_meridian

    intersects_180_meridian = intersects180_meridian
