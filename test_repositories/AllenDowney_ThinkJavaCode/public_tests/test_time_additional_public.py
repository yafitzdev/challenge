import pytest

try:
    from src.ch11.time import Time
except ImportError:
    from ch11.time import Time

def test_time_to_seconds_and_conversion():
    t = Time(6, 4, 15.0)
    seconds = Time.time_to_seconds(t)
    assert abs(seconds - (6*3600 + 4*60 + 15.0)) < 1e-8

    t2 = Time.seconds_to_time(3678.5)
    assert t2.hour == 1
    assert t2.minute == 1
    assert abs(t2.second - 18.5) < 1e-8

def test_subtract_time():
    t1 = Time(7, 10, 15.0)
    t2 = Time(4, 20, 15.0)
    diff = Time.subtract(t1, t2)
    assert diff.hour == 2
    assert diff.minute == 50
    assert abs(diff.second - 0.0) < 1e-8