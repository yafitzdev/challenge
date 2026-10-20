from src.geohash.util.geohash_size_table import GeoHashSizeTable

def test_width_height_public():
    assert GeoHashSizeTable.width_degrees_for_precision(1) == pytest.approx(125.0, abs=0.001)
    assert GeoHashSizeTable.width_degrees_for_precision(3) == pytest.approx(5.0, abs=0.001)
    assert GeoHashSizeTable.width_degrees_for_precision(7) == pytest.approx(0.019, abs=0.001)
    assert GeoHashSizeTable.height_degrees_for_precision(1) == pytest.approx(625.0, abs=0.001)
    assert GeoHashSizeTable.height_degrees_for_precision(7) == pytest.approx(0.019, abs=0.001)

def test_max_precision_and_zero_public():
    assert GeoHashSizeTable.width_degrees_for_precision(12) == pytest.approx(0.0006, abs=0.0001)
    assert GeoHashSizeTable.height_degrees_for_precision(12) == pytest.approx(0.0006, abs=0.0001)
    assert GeoHashSizeTable.width_degrees_for_precision(0) == pytest.approx(360.0, abs=0.001)
    assert GeoHashSizeTable.height_degrees_for_precision(0) == pytest.approx(180.0, abs=0.001)