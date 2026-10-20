import pytest

from src.signaturepad.utils import Bezier, TimedPoint

def test_set_and_point_public():
    sp = TimedPoint().set(2, -2)
    c1 = TimedPoint().set(4, 15)
    c2 = TimedPoint().set(20, 10)
    ep = TimedPoint().set(25, -4)
    bezier = Bezier()
    bezier.set(sp, c1, c2, ep)
    assert bezier.startPoint == sp
    assert bezier.control1 == c1
    assert bezier.control2 == c2
    assert bezier.endPoint == ep

    point_x = bezier.point(0.25, 2, 4, 20, 25)
    assert 2 < point_x < 25

    point_y = bezier.point(0.75, -2, 15, 10, -4)
    assert -4 < point_y < 15

def test_length_different_straight_line():
    sp = TimedPoint().set(10, 10)
    c1 = TimedPoint().set(10, 10)
    c2 = TimedPoint().set(30, 10)
    ep = TimedPoint().set(30, 10)
    bezier = Bezier()
    bezier.set(sp, c1, c2, ep)
    length = bezier.length()
    assert 19 < length < 21, f"Length should be about 20, got: {length}"

def test_length_public_curved():
    sp = TimedPoint().set(5, 5)
    c1 = TimedPoint().set(5, 25)
    c2 = TimedPoint().set(25, 25)
    ep = TimedPoint().set(25, 5)
    bezier = Bezier()
    bezier.set(sp, c1, c2, ep)
    length = bezier.length()
    assert length > 20