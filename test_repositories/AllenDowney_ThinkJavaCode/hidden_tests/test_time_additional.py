import pytest
import io
import sys

try:
    from src.ch11.time import Time
except ImportError:
    from ch11.time import Time

def test_print_time_output(capsys):
    t = Time(12, 34, 56.7)
    Time.print_time(t)
    out = capsys.readouterr().out.replace('\r', '')
    assert "12" in out, "Should print hour"
    assert "34" in out, "Should print minute"
    assert "56.7" in out, "Should print second"

def test_add_instance_with_multiple_rollovers():
    t1 = Time(22, 58, 58.0)
    t2 = Time(1, 2, 62.5)
    sumt = t1.add(t2)
    # Matching Java's expected: "24:01:60.5\n"
    assert str(sumt) == "24:01:60.5\n"

def test_increment_looping_multiple_hours():
    t = Time(0, 0, 0.0)
    t.increment(3661.5)
    assert str(t) == "01:01:01.5\n"

def test_equals_with_null_and_self():
    t = Time(2, 3, 4.5)
    assert t == t  # Self-check; in Python should always be true (id)