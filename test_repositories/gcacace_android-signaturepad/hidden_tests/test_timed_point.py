import pytest
import time

from src.signaturepad.utils import TimedPoint

def test_set():
    tp = TimedPoint()
    ret = tp.set(5, 10)
    assert ret is tp
    assert abs(tp.x - 5) < 0.01
    assert abs(tp.y - 10) < 0.01

def test_distance_to():
    t1 = TimedPoint().set(0, 0)
    t2 = TimedPoint().set(3, 4)
    dist = t1.distanceTo(t2)
    assert abs(dist - 5.0) < 0.001

def test_velocity_from_positive_diff():
    t1 = TimedPoint().set(0, 0)
    time.sleep(0.002)  # Sleep 2 milliseconds
    t2 = TimedPoint().set(3, 4)
    velocity = t2.velocityFrom(t1)
    assert velocity > 0

def test_velocity_from_zero_diff():
    t1 = TimedPoint().set(0, 0)
    t2 = TimedPoint()
    t2.x = 3
    t2.y = 4
    t2.timestamp = t1.timestamp  # same timestamp as t1
    velocity = t2.velocityFrom(t1)
    assert abs(velocity - 5.0) < 0.001

def test_velocity_nan_infinite():
    t1 = TimedPoint()
    t1.x = t1.y = 0
    t1.timestamp = 100
    t2 = TimedPoint()
    t2.x = t2.y = 0
    t2.timestamp = 200
    velocity = t2.velocityFrom(t1)
    assert velocity == 0