class GeoHashQuery:
    """Interface: contains(GeoHash|WGS84Point), get_search_hashes(), get_wkt_box()."""

    def contains(self, obj):
        raise NotImplementedError

    def get_search_hashes(self):
        raise NotImplementedError

    def get_wkt_box(self):
        raise NotImplementedError
