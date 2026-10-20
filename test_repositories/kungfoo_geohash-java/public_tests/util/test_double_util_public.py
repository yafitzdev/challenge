from src.geohash.util.double_util import DoubleUtil

def test_positive_value_public():
    assert DoubleUtil.remainder_with_fix(27.0, 360) == pytest.approx(27.0, 1e-5)
    assert DoubleUtil.remainder_with_fix(919.5, 360) == pytest.approx(199.5, 1e-5)

def test_negative_value_public():
    assert DoubleUtil.remainder_with_fix(-39.8, 360) == pytest.approx(320.2, 1e-5)
    assert DoubleUtil.remainder_with_fix(-248.9, 360) == pytest.approx(111.1, 1e-5)