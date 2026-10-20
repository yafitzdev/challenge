from ..bounding_box import BoundingBox


class TwoGeoHashBoundingBox:
    @staticmethod
    def with_character_precision(bbox, number_of_characters):
        from ..geohash import GeoHash
        sw = GeoHash.with_character_precision(bbox.get_south_latitude(), bbox.get_west_longitude(), number_of_characters)
        ne = GeoHash.with_character_precision(bbox.get_north_latitude(), bbox.get_east_longitude(), number_of_characters)
        return TwoGeoHashBoundingBox(sw, ne)

    @staticmethod
    def with_bit_precision(bbox, number_of_bits):
        from ..geohash import GeoHash
        sw = GeoHash.with_bit_precision(bbox.get_south_latitude(), bbox.get_west_longitude(), number_of_bits)
        ne = GeoHash.with_bit_precision(bbox.get_north_latitude(), bbox.get_east_longitude(), number_of_bits)
        return TwoGeoHashBoundingBox(sw, ne)

    def __init__(self, south_west_corner, north_east_corner):
        from ..geohash import GeoHash
        if south_west_corner.significant_bits() != north_east_corner.significant_bits():
            raise ValueError("Does it make sense to iterate between hashes that have different precisions?")
        self._south_west_corner = GeoHash.from_long_value(south_west_corner.long_value(),
                                                          south_west_corner.significant_bits())
        self._north_east_corner = GeoHash.from_long_value(north_east_corner.long_value(),
                                                          north_east_corner.significant_bits())
        self._bounding_box = BoundingBox(south_west_corner.get_bounding_box().get_south_latitude(),
                                         north_east_corner.get_bounding_box().get_north_latitude(),
                                         south_west_corner.get_bounding_box().get_west_longitude(),
                                         north_east_corner.get_bounding_box().get_east_longitude())

    def get_bounding_box(self):
        return self._bounding_box

    def get_south_west_corner(self):
        return self._south_west_corner

    def get_north_east_corner(self):
        return self._north_east_corner

    def to_base32(self):
        return self._south_west_corner.to_base32() + self._north_east_corner.to_base32()
