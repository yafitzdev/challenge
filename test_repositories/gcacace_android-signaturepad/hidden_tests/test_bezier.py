import pytest

from src.signaturepad.utils import Bezier, TimedPoint

def test_set_and_point():
    sp = TimedPoint().set(0, 0)
    c1 = TimedPoint().set(5, 5)
    c2 = TimedPoint().set(10, 5)
    ep = TimedPoint().set(10, 0)
    bezier = Bezier()
    bezier.set(sp, c1, c2, ep)
    assert bezier.startPoint == sp
    assert bezier.control1 == c1
    assert bezier.control2 == c2
    assert bezier.endPoint == ep

    point_x = bezier.point(0.5, 0, 5, 10, 10)
    assert 0 < point_x < 10

    point_y = bezier.point(0.5, 0, 5, 5, 0)
    assert 0 <= point_y <= 5

def test_length_straight_line():
    sp = TimedPoint().set(0, 0)
    c1 = TimedPoint().set(0, 0)
    c2 = TimedPoint().set(10, 0)
    ep = TimedPoint().set(10, 0)
    bezier = Bezier()
    bezier.set(sp, c1, c2, ep)
    length = bezier.length()
    assert 9 < length < 11, f"Length should be about 10, got: {length}"

def test_length_curved():
    sp = TimedPoint().set(0, 0)
    c1 = TimedPoint().set(0, 10)
    c2 = TimedPoint().set(10, 10)
    ep = TimedPoint().set(10, 0)
    bezier = Bezier()
    bezier.set(sp, c1, c2, ep)
    length = bezier.length()
    assert length > 10