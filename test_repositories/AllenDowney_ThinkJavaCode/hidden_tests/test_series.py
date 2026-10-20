import pytest

# Assumes series.py is imported from src.ap01 or similar location;
# you must have the implementation in sys.path for this import to actually resolve.
try:
    from src.ap01.series import Series
except ImportError:
    # fallback for flat src
    from ap01.series import Series

def test_fibonacci_base_cases():
    assert Series.fibonacci(1) == 1
    assert Series.fibonacci(2) == 1

def test_fibonacci_small_n():
    assert Series.fibonacci(3) == 2
    assert Series.fibonacci(4) == 3
    assert Series.fibonacci(5) == 5

def test_fibonacci_larger_n():
    assert Series.fibonacci(8) == 21

# Legacy JUnit-style simple test, just for completeness
def test_fibonacci_example_legacy():
    assert Series.fibonacci(1) == 1
    assert Series.fibonacci(2) == 1
    assert Series.fibonacci(3) == 2