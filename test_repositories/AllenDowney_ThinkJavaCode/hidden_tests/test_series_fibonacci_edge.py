import pytest

try:
    from src.ap01.series import Series
except ImportError:
    from ap01.series import Series

def test_fibonacci_zero_and_negative():
    # Defensive: Should error or recurse infinitely for bad input (simulate StackOverflowError)
    # In Python, may trigger RecursionError for bad recursion
    with pytest.raises(RecursionError):
        Series.fibonacci(0)
    with pytest.raises(RecursionError):
        Series.fibonacci(-5)