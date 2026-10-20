import pytest

try:
    from src.ap01.series import Series
except ImportError:
    from ap01.series import Series

def test_fibonacci_low():
    assert Series.fibonacci(7) == 13
    assert Series.fibonacci(8) == 21

def test_fibonacci_high_different_inputs():
    assert Series.fibonacci(10) == 55
    assert Series.fibonacci(11) == 89
    assert Series.fibonacci(12) == 144

def test_fibonacci_edge():
    assert Series.fibonacci(1) == 1
    assert Series.fibonacci(2) == 1