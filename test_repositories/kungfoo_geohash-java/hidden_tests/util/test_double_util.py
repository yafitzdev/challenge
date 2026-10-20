from src.geohash.util.double_util import DoubleUtil

def test_positive_value():
    assert DoubleUtil.remainder_with_fix(58.1541, 360) == pytest.approx(58.1541, 1e-5)
    assert DoubleUtil.remainder_with_fix(453.1541, 360) == pytest.approx(93.1541, 1e-5)

def test_negative_value():
    assert DoubleUtil.remainder_with_fix(-58.1541, 360) == pytest.approx(301.8459, 1e-5)
    assert DoubleUtil.remainder_with_fix(-453.1541, 360) == pytest.approx(266.8459, 1e-5)