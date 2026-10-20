"""Port of the Java test helper ch.hsr.geohash.util.RandomGeohashes."""
from .._java import JavaRandom


class RandomGeohashes:
    _rand = JavaRandom(9817298371)

    @staticmethod
    def full_range():
        from ..geohash import GeoHash
        rand = JavaRandom()
        hashes = []
        lat = -90.0
        while lat <= 90:
            lon = -180.0
            while lon <= 180:
                for precision_chars in range(6, 13):
                    hashes.append(GeoHash.with_character_precision(lat, lon, precision_chars))
                lon += rand.next_double() + 1.54
            lat += rand.next_double() + 1.45
        return hashes

    @staticmethod
    def create():
        from ..geohash import GeoHash
        return GeoHash.with_bit_precision(RandomGeohashes._random_latitude(), RandomGeohashes._random_longitude(),
                                          RandomGeohashes._random_precision())

    @staticmethod
    def create_with_5_bits_precision():
        from ..geohash import GeoHash
        return GeoHash.with_character_precision(RandomGeohashes._random_latitude(),
                                                RandomGeohashes._random_longitude(),
                                                RandomGeohashes._random_character_precision())

    @staticmethod
    def create_with_precision(precision):
        from ..geohash import GeoHash
        return GeoHash.with_bit_precision(RandomGeohashes._random_latitude(), RandomGeohashes._random_longitude(),
                                          precision)

    @staticmethod
    def _random_latitude():
        return (RandomGeohashes._rand.next_double() - 0.5) * 180

    @staticmethod
    def _random_longitude():
        return (RandomGeohashes._rand.next_double() - 0.5) * 360

    @staticmethod
    def _random_precision():
        return RandomGeohashes._rand.next_int(60) + 5

    @staticmethod
    def _random_character_precision():
        return RandomGeohashes._rand.next_int(12) + 1
