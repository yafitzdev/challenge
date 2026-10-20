import pytest

from src.signaturepad.utils import ControlTimedPoints, TimedPoint

def test_set():
    c1 = TimedPoint().set(1, 2)
    c2 = TimedPoint().set(3, 4)
    control = ControlTimedPoints()
    ret = control.set(c1, c2)
    assert ret is control
    assert control.c1 == c1
    assert control.c2 == c2