import math

from .wgs84point import WGS84Point
from .bounding_box import BoundingBox
from ._java import to_long, to_int, shl, ushr, sar, MASK64

_BITS = (16, 8, 4, 2, 1)
_BASE32_BITS = 5
_BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"
_DECODE = {c: i for i, c in enumerate(_BASE32)}


def _java_compare(a, b):
    return -1 if a < b else (1 if a > b else 0)


class GeoHash:
    MAX_BIT_PRECISION = 64
    MAX_CHARACTER_PRECISION = 12
    FIRST_BIT_FLAGGED = to_long(0x8000000000000000)

    def __init__(self, latitude=None, longitude=None, desired_precision=None):
        self.bits = 0
        self._point = None
        self._bounding_box = None
        self._significant_bits = 0
        if latitude is None:
            return
        # private GeoHash(double latitude, double longitude, int desiredPrecision)
        self._point = WGS84Point(latitude, longitude)
        latitude = float(latitude)
        longitude = float(longitude)
        desired_precision = min(desired_precision, GeoHash.MAX_BIT_PRECISION)
        is_even_bit = True
        latitude_range = [-90.0, 90.0]
        longitude_range = [-180.0, 180.0]
        while self._significant_bits < desired_precision:
            if is_even_bit:
                self._divide_range_encode(longitude, longitude_range)
            else:
                self._divide_range_encode(latitude, latitude_range)
            is_even_bit = not is_even_bit
        GeoHash._set_bounding_box(self, latitude_range, longitude_range)
        self.bits = shl(self.bits, GeoHash.MAX_BIT_PRECISION - desired_precision)

    # ---- factories ----
    @staticmethod
    def with_character_precision(latitude, longitude, number_of_characters):
        if number_of_characters > GeoHash.MAX_CHARACTER_PRECISION:
            raise ValueError("A geohash can only be %d character long." % GeoHash.MAX_CHARACTER_PRECISION)
        desired = number_of_characters * 5 if number_of_characters * 5 <= 60 else 60
        return GeoHash(latitude, longitude, desired)

    @staticmethod
    def with_bit_precision(latitude, longitude, number_of_bits):
        if number_of_bits < 0:
            raise ValueError("A Geohash can't be of negative bits long!")
        if number_of_bits > GeoHash.MAX_BIT_PRECISION:
            raise ValueError("A Geohash can only be %d bits long!" % GeoHash.MAX_BIT_PRECISION)
        if abs(latitude) > 90.0 or abs(longitude) > 180.0:
            raise ValueError("Can't have lat/lon values out of (-90,90)/(-180/180)")
        return GeoHash(latitude, longitude, number_of_bits)

    @staticmethod
    def from_binary_string(binary_string):
        geohash = GeoHash()
        for ch in binary_string:
            if ch == "1":
                geohash.add_on_bit_to_end()
            elif ch == "0":
                geohash.add_off_bit_to_end()
            else:
                raise ValueError(binary_string + " is not a valid geohash as a binary string")
        geohash.bits = shl(geohash.bits, GeoHash.MAX_BIT_PRECISION - geohash._significant_bits)
        latitude_bits = geohash.get_right_aligned_latitude_bits()
        longitude_bits = geohash.get_right_aligned_longitude_bits()
        return geohash.recombine_lat_lon_bits_to_hash(latitude_bits, longitude_bits)

    @staticmethod
    def from_geohash_string(geohash):
        latitude_range = [-90.0, 90.0]
        longitude_range = [-180.0, 180.0]
        is_even_bit = True
        h = GeoHash()
        for c in geohash:
            cd = _DECODE.get(c, -1)
            if cd < 0:
                raise ValueError("Invalid character character '%s' in geohash '%s'!" % (c, geohash))
            for j in range(_BASE32_BITS):
                mask = _BITS[j]
                if is_even_bit:
                    GeoHash._divide_range_decode(h, longitude_range, (cd & mask) != 0)
                else:
                    GeoHash._divide_range_decode(h, latitude_range, (cd & mask) != 0)
                is_even_bit = not is_even_bit
        latitude = (latitude_range[0] + latitude_range[1]) / 2
        longitude = (longitude_range[0] + longitude_range[1]) / 2
        h._point = WGS84Point(latitude, longitude)
        GeoHash._set_bounding_box(h, latitude_range, longitude_range)
        h.bits = shl(h.bits, GeoHash.MAX_BIT_PRECISION - h._significant_bits)
        return h

    @staticmethod
    def from_long_value(hash_val, significant_bits):
        latitude_range = [-90.0, 90.0]
        longitude_range = [-180.0, 180.0]
        is_even_bit = True
        h = GeoHash()
        binary_string = format(hash_val & MASK64, "b").rjust(GeoHash.MAX_BIT_PRECISION, "0")
        for j in range(significant_bits):
            if is_even_bit:
                GeoHash._divide_range_decode(h, longitude_range, binary_string[j] != "0")
            else:
                GeoHash._divide_range_decode(h, latitude_range, binary_string[j] != "0")
            is_even_bit = not is_even_bit
        latitude = (latitude_range[0] + latitude_range[1]) / 2
        longitude = (longitude_range[0] + longitude_range[1]) / 2
        h._point = WGS84Point(latitude, longitude)
        GeoHash._set_bounding_box(h, latitude_range, longitude_range)
        h.bits = shl(h.bits, GeoHash.MAX_BIT_PRECISION - h._significant_bits)
        return h

    @staticmethod
    def geo_hash_string_with_character_precision(latitude, longitude, number_of_characters):
        return GeoHash.with_character_precision(latitude, longitude, number_of_characters).to_base32()

    @staticmethod
    def _set_bounding_box(h, latitude_range, longitude_range):
        h._bounding_box = BoundingBox(latitude_range[0], latitude_range[1], longitude_range[0], longitude_range[1])

    # ---- navigation ----
    def next(self, step=1):
        return GeoHash.from_ord(to_long(self.ord() + step), self._significant_bits)

    def prev(self):
        return self.next(-1)

    def ord(self):
        insignificant_bits = GeoHash.MAX_BIT_PRECISION - self._significant_bits
        return ushr(self.bits, insignificant_bits)

    def get_character_precision(self):
        if self._significant_bits % 5 != 0:
            raise RuntimeError("precision of GeoHash is not divisble by 5: " + str(self))
        return self._significant_bits // 5

    @staticmethod
    def from_ord(ord_, significant_bits):
        insignificant_bits = GeoHash.MAX_BIT_PRECISION - significant_bits
        return GeoHash.from_long_value(shl(ord_, insignificant_bits), significant_bits)

    @staticmethod
    def steps_between(one, two):
        if one.significant_bits() != two.significant_bits():
            raise ValueError("It is only valid to compare the number of steps between two hashes if they have "
                             "the same number of significant bits")
        return to_long(two.ord() - one.ord())

    def _divide_range_encode(self, value, rng):
        mid = (rng[0] + rng[1]) / 2
        if value >= mid:
            self.add_on_bit_to_end()
            rng[0] = mid
        else:
            self.add_off_bit_to_end()
            rng[1] = mid

    @staticmethod
    def _divide_range_decode(h, rng, b):
        mid = (rng[0] + rng[1]) / 2
        if b:
            h.add_on_bit_to_end()
            rng[0] = mid
        else:
            h.add_off_bit_to_end()
            rng[1] = mid

    def get_adjacent(self):
        northern = self.get_northern_neighbour()
        eastern = self.get_eastern_neighbour()
        southern = self.get_southern_neighbour()
        western = self.get_western_neighbour()
        return [northern, northern.get_eastern_neighbour(), eastern, southern.get_eastern_neighbour(),
                southern, southern.get_western_neighbour(), western, northern.get_western_neighbour()]

    def significant_bits(self):
        return self._significant_bits

    def long_value(self):
        return self.bits

    def to_base32(self):
        if self._significant_bits % 5 != 0:
            raise RuntimeError("Cannot convert a geohash to base32 if the precision is not a multiple of 5.")
        buf = []
        first_five_bits_mask = to_long(0xf800000000000000)
        bits_copy = self.bits
        partial_chunks = int(math.ceil(self._significant_bits / 5))
        for _ in range(partial_chunks):
            pointer = to_int(ushr(bits_copy & first_five_bits_mask, 59))
            buf.append(_BASE32[pointer])
            bits_copy = shl(bits_copy, 5)
        return "".join(buf)

    def within(self, bounding_box):
        return (self.bits & bounding_box._mask()) == bounding_box.bits

    def contains(self, point):
        return self._bounding_box.contains(point)

    def get_originating_point(self):
        return self._point

    def get_bounding_box_center(self):
        return self._bounding_box.get_center()

    def get_bounding_box(self):
        return self._bounding_box

    def encloses_circle_around_point(self, point, radius):
        return False

    def recombine_lat_lon_bits_to_hash(self, lat_bits, lon_bits):
        h = GeoHash()
        is_even_bit = False
        lat_bits[0] = shl(lat_bits[0], GeoHash.MAX_BIT_PRECISION - lat_bits[1])
        lon_bits[0] = shl(lon_bits[0], GeoHash.MAX_BIT_PRECISION - lon_bits[1])
        latitude_range = [-90.0, 90.0]
        longitude_range = [-180.0, 180.0]
        F = GeoHash.FIRST_BIT_FLAGGED
        for _ in range(lat_bits[1] + lon_bits[1]):
            if is_even_bit:
                GeoHash._divide_range_decode(h, latitude_range, (lat_bits[0] & F) == F)
                lat_bits[0] = shl(lat_bits[0], 1)
            else:
                GeoHash._divide_range_decode(h, longitude_range, (lon_bits[0] & F) == F)
                lon_bits[0] = shl(lon_bits[0], 1)
            is_even_bit = not is_even_bit
        h.bits = shl(h.bits, GeoHash.MAX_BIT_PRECISION - h._significant_bits)
        GeoHash._set_bounding_box(h, latitude_range, longitude_range)
        h._point = h._bounding_box.get_center()
        return h

    def get_northern_neighbour(self):
        lat = self.get_right_aligned_latitude_bits()
        lon = self.get_right_aligned_longitude_bits()
        lat[0] = to_long(lat[0] + 1)
        lat[0] = self._mask_last_n_bits(lat[0], lat[1])
        return self.recombine_lat_lon_bits_to_hash(lat, lon)

    def get_southern_neighbour(self):
        lat = self.get_right_aligned_latitude_bits()
        lon = self.get_right_aligned_longitude_bits()
        lat[0] = to_long(lat[0] - 1)
        lat[0] = self._mask_last_n_bits(lat[0], lat[1])
        return self.recombine_lat_lon_bits_to_hash(lat, lon)

    def get_eastern_neighbour(self):
        lat = self.get_right_aligned_latitude_bits()
        lon = self.get_right_aligned_longitude_bits()
        lon[0] = to_long(lon[0] + 1)
        lon[0] = self._mask_last_n_bits(lon[0], lon[1])
        return self.recombine_lat_lon_bits_to_hash(lat, lon)

    def get_western_neighbour(self):
        lat = self.get_right_aligned_latitude_bits()
        lon = self.get_right_aligned_longitude_bits()
        lon[0] = to_long(lon[0] - 1)
        lon[0] = self._mask_last_n_bits(lon[0], lon[1])
        return self.recombine_lat_lon_bits_to_hash(lat, lon)

    def get_right_aligned_latitude_bits(self):
        copy_of_bits = shl(self.bits, 1)
        n = self.get_number_of_lat_lon_bits()[0]
        return [self._extract_every_second_bit(copy_of_bits, n), n]

    def get_right_aligned_longitude_bits(self):
        copy_of_bits = self.bits
        n = self.get_number_of_lat_lon_bits()[1]
        return [self._extract_every_second_bit(copy_of_bits, n), n]

    def _extract_every_second_bit(self, copy_of_bits, number_of_bits):
        value = 0
        F = GeoHash.FIRST_BIT_FLAGGED
        for _ in range(number_of_bits):
            if (copy_of_bits & F) == F:
                value |= 0x1
            value = shl(value, 1)
            copy_of_bits = shl(copy_of_bits, 2)
        return ushr(value, 1)

    def get_number_of_lat_lon_bits(self):
        sb = self._significant_bits
        if sb % 2 == 0:
            return [sb // 2, sb // 2]
        return [sb // 2, sb // 2 + 1]

    def add_on_bit_to_end(self):
        self._significant_bits += 1
        self.bits = shl(self.bits, 1) | 0x1

    def add_off_bit_to_end(self):
        self._significant_bits += 1
        self.bits = shl(self.bits, 1)

    def __str__(self):
        bin_str = format(self.bits & MASK64, "b").rjust(64, "0")
        if self._significant_bits % 5 == 0:
            return "%s -> %s -> %s" % (bin_str, self._bounding_box, self.to_base32())
        return "%s -> %s, bits: %d" % (bin_str, self._bounding_box, self._significant_bits)

    __repr__ = __str__

    def to_binary_string(self):
        out = []
        bits_copy = self.bits
        F = GeoHash.FIRST_BIT_FLAGGED
        for _ in range(self._significant_bits):
            out.append("1" if (bits_copy & F) == F else "0")
            bits_copy = shl(bits_copy, 1)
        return "".join(out)

    def __eq__(self, obj):
        if obj is self:
            return True
        if isinstance(obj, GeoHash):
            return obj._significant_bits == self._significant_bits and obj.bits == self.bits
        return False

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        f = 17
        f = to_int(31 * f + to_int(self.bits ^ ushr(self.bits, 32)))
        f = to_int(31 * f + self._significant_bits)
        return f

    hash_code = __hash__

    def _mask(self):
        if self._significant_bits == 0:
            return 0
        return sar(GeoHash.FIRST_BIT_FLAGGED, self._significant_bits - 1)

    @staticmethod
    def _mask_last_n_bits(value, n):
        mask = to_long(0xffffffffffffffff)
        mask = ushr(mask, GeoHash.MAX_BIT_PRECISION - n)
        return value & mask

    def compare_to(self, o):
        F = GeoHash.FIRST_BIT_FLAGGED
        bits_cmp = _java_compare(to_long(self.bits ^ F), to_long(o.bits ^ F))
        if bits_cmp != 0:
            return bits_cmp
        return _java_compare(self._significant_bits, o._significant_bits)

    def __lt__(self, o):
        return self.compare_to(o) < 0

    def __le__(self, o):
        return self.compare_to(o) <= 0

    def __gt__(self, o):
        return self.compare_to(o) > 0

    def __ge__(self, o):
        return self.compare_to(o) >= 0
