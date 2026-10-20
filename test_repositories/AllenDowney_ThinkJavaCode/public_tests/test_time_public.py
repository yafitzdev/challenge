import pytest

try:
    from src.ch11.time import Time
except ImportError:
    from ch11.time import Time

def test_to_string_and_constructor_public():
    t = Time(3, 7, 15.5)
    assert str(t) == "03:07:15.5\n"

def test_add_static_public():
    t1 = Time(5, 10, 10.5)
    t2 = Time(6, 20, 50.5)
    sumt = Time.add(t1, t2)
    assert sumt.hour == 11
    assert sumt.minute == 30
    assert abs(sumt.second - 61.0) < 1e-8

def test_add_instance_with_no_rollover_public():
    t1 = Time(2, 10, 20.0)
    t2 = Time(2, 40, 25.0)
    sumt = t1.add(t2)
    assert str(sumt) == "04:50:45.0\n"

def test_increment_simple_public():
    t = Time(1, 2, 3.0)
    t.increment(10.0)
    assert str(t) == "01:02:13.0\n"

def test_increment_with_minute_rollover_public():
    t = Time(1, 59, 59.0)
    t.increment(2.5)
    assert str(t) == "02:00:01.5\n"