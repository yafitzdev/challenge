class GeoHashSizeTable:
    NUM_BITS = 64

    @staticmethod
    def d_lat(bits):
        return 180.0 / (2.0 ** (bits // 2))

    @staticmethod
    def d_lon(bits):
        return 360.0 / (2.0 ** ((bits + 1) // 2))

    @staticmethod
    def number_of_bits_for_overlapping_geohash(bounding_box):
        bits = 63
        height = bounding_box.get_latitude_size()
        width = bounding_box.get_longitude_size()
        while (_D_LAT[bits] < height or _D_LON[bits] < width) and bits > 0:
            bits -= 1
        return bits


_D_LAT = [GeoHashSizeTable.d_lat(i) for i in range(GeoHashSizeTable.NUM_BITS)]
_D_LON = [GeoHashSizeTable.d_lon(i) for i in range(GeoHashSizeTable.NUM_BITS)]
