import pytest

try:
    from src.ch11.time import Time
except ImportError:
    from ch11.time import Time

def test_custom_to_string_public():
    t = Time(2, 45, 30.0)
    assert str(t) == "02:45:30.0\n"

def test_add_and_increment_with_diff_data_public():
    t1 = Time(3, 15, 25.0)
    t2 = Time(4, 25, 35.0)
    sumt = Time.add(t1, t2)
    assert sumt.hour == 7
    assert sumt.minute == 40
    assert abs(sumt.second - 60.0) < 1e-8

    t1.increment(36.5)
    assert str(t1) == "03:16:01.5\n"