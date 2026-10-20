import pytest

try:
    from src.ap01.series import Series
except ImportError:
    from ap01.series import Series

def test_geometric_series_different_data():
    # a=3, r=2, n=4 -> 3*(1+2+4+8)=45
    assert Series.geometric_series_sum(3, 2, 4) == 45
    # a=1, r=10, n=3 -> 1*(1+10+100)=111
    assert Series.geometric_series_sum(1, 10, 3) == 111

def test_arithmetic_series_different_data():
    # a=2, d=5, n=4 -> 2+7+12+17=38
    assert Series.arithmetic_series_sum(2, 5, 4) == 38
    # a=3, d=0, n=5 -> 3+3+3+3+3 = 15
    assert Series.arithmetic_series_sum(3, 0, 5) == 15