import pytest

try:
    from src.ch11.time import Time
except ImportError:
    from ch11.time import Time

def test_default_constructor():
    t = Time()
    assert str(t) == "00:00:00.0\n"

def test_parameterized_constructor_and_to_string():
    t = Time(9, 15, 7.7)
    assert str(t) == "09:15:07.7\n"

def test_equals_true_and_false():
    t1 = Time(2, 5, 10.0)
    t2 = Time(2, 5, 10.0)
    t3 = Time(3, 5, 10.0)
    assert t1 == t2
    assert t1 != t3

def test_add_static():
    t1 = Time(1, 20, 30.0)
    t2 = Time(2, 40, 15.5)
    sumt = Time.add(t1, t2)
    assert str(sumt) == "03:60:45.5\n"

def test_add_instance_no_rollover():
    t1 = Time(1, 20, 10.0)
    t2 = Time(2, 10, 30.0)
    sumt = t1.add(t2)
    assert str(sumt) == "03:30:40.0\n"

def test_add_instance_with_second_rollover():
    t1 = Time(1, 50, 40.0)
    t2 = Time(0, 5, 25.0)
    sumt = t1.add(t2)
    assert str(sumt) == "01:56:05.0\n"

def test_add_instance_with_minute_rollover():
    t1 = Time(1, 55, 50.0)
    t2 = Time(0, 6, 15.0)
    sumt = t1.add(t2)
    assert str(sumt) == "02:02:05.0\n"

def test_increment_no_rollover():
    t = Time(2, 15, 50.0)
    t.increment(5.5)
    assert str(t) == "02:15:55.5\n"

def test_increment_seconds_to_minute_rollover():
    t = Time(0, 44, 50.0)
    t.increment(14.0)
    assert str(t) == "00:45:04.0\n"

def test_increment_seconds_and_minute_rollover():
    t = Time(1, 59, 55.0)
    t.increment(10.0)
    assert str(t) == "02:00:05.0\n"