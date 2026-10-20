from ._java import java_double_to_string, double_hash, to_int


class WGS84Point:
    def __init__(self, latitude, longitude=None):
        if isinstance(latitude, WGS84Point) and longitude is None:
            other = latitude
            latitude, longitude = other._latitude, other._longitude
        self._latitude = float(latitude)
        self._longitude = float(longitude)
        if abs(self._latitude) > 90 or abs(self._longitude) > 180:
            raise ValueError("The supplied coordinates " + str(self) + " are out of range.")

    def get_latitude(self):
        return self._latitude

    def get_longitude(self):
        return self._longitude

    def __str__(self):
        return "(" + java_double_to_string(self._latitude) + "," + java_double_to_string(self._longitude) + ")"

    __repr__ = __str__

    def __eq__(self, obj):
        if isinstance(obj, WGS84Point):
            return self._latitude == obj._latitude and self._longitude == obj._longitude
        return False

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        result = 42
        result = to_int(31 * result + double_hash(self._latitude))
        result = to_int(31 * result + double_hash(self._longitude))
        return result

    hash_code = __hash__
