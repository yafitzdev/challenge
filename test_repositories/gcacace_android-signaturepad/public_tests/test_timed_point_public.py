import pytest
import time

from src.signaturepad.utils import TimedPoint

def test_set_public():
    tp = TimedPoint()
    ret = tp.set(-7.2, 8.19)
    assert ret is tp
    assert abs(tp.x + 7.2) < 0.01
    assert abs(tp.y - 8.19) < 0.01

def test_distance_to_public():
    t1 = TimedPoint().set(1, 1)
    t2 = TimedPoint().set(4, 5)
    dist = t1.distanceTo(t2)
    assert abs(dist - 5.0) < 0.001

def test_velocity_from_positive_diff_public():
    t1 = TimedPoint().set(2, 3)
    time.sleep(0.002)  # 2 milliseconds
    t2 = TimedPoint().set(7, 11)
    velocity = t2.velocityFrom(t1)
    assert velocity > 0

def test_velocity_from_zero_diff_public():
    t1 = TimedPoint().set(3, 4)
    t2 = TimedPoint()
    t2.x = 6
    t2.y = 8
    t2.timestamp = t1.timestamp
    velocity = t2.velocityFrom(t1)
    assert abs(velocity - 5.0) < 0.001

def test_velocity_nan_infinite_public():
    t1 = TimedPoint()
    t1.x = t1.y = 10
    t1.timestamp = 500
    t2 = TimedPoint()
    t2.x = t2.y = 10
    t2.timestamp = 600
    velocity = t2.velocityFrom(t1)
    assert velocity == 0