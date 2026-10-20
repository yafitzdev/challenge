import pytest

from src.signaturepad.utils import ControlTimedPoints, TimedPoint

def test_set_with_different_points():
    c1 = TimedPoint().set(-5.5, 42.42)
    c2 = TimedPoint().set(100, -200)
    control = ControlTimedPoints()
    ret = control.set(c1, c2)
    assert ret is control
    assert control.c1 == c1
    assert control.c2 == c2