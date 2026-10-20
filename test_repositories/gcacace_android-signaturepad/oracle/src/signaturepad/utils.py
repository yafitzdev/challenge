"""Python port of com.github.gcacace.signaturepad.utils (TimedPoint, ControlTimedPoints, Bezier)."""
import math
import struct
import time


def _f32(v):
    """Round a Python float to Java float (32-bit) precision."""
    v = float(v)
    if math.isnan(v) or math.isinf(v):
        return v
    try:
        return struct.unpack('f', struct.pack('f', v))[0]
    except OverflowError:
        return math.copysign(math.inf, v)


def _current_time_millis():
    return int(time.time() * 1000)


class TimedPoint(object):
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.timestamp = 0

    def set(self, x, y):
        self.x = _f32(x)
        self.y = _f32(y)
        self.timestamp = _current_time_millis()
        return self

    def velocityFrom(self, start):
        diff = int(self.timestamp) - int(start.timestamp)
        if diff <= 0:
            diff = 1
        velocity = _f32(self.distanceTo(start) / diff)
        if math.isinf(velocity) or math.isnan(velocity):
            velocity = 0.0
        return velocity

    def distanceTo(self, point):
        return _f32(math.sqrt(math.pow(_f32(point.x - self.x), 2) + math.pow(_f32(point.y - self.y), 2)))


class ControlTimedPoints(object):
    def __init__(self):
        self.c1 = None
        self.c2 = None

    def set(self, c1, c2):
        self.c1 = c1
        self.c2 = c2
        return self


class Bezier(object):
    def __init__(self):
        self.startPoint = None
        self.control1 = None
        self.control2 = None
        self.endPoint = None

    def set(self, startPoint, control1, control2, endPoint):
        self.startPoint = startPoint
        self.control1 = control1
        self.control2 = control2
        self.endPoint = endPoint
        return self

    def length(self):
        steps = 10
        length = 0.0
        px = py = 0.0
        for i in range(steps + 1):
            t = _f32(float(i) / steps)
            cx = self.point(t, self.startPoint.x, self.control1.x, self.control2.x, self.endPoint.x)
            cy = self.point(t, self.startPoint.y, self.control1.y, self.control2.y, self.endPoint.y)
            if i > 0:
                x_diff = cx - px
                y_diff = cy - py
                length = _f32(length + math.sqrt(x_diff * x_diff + y_diff * y_diff))
            px = cx
            py = cy
        return length

    def point(self, t, start, c1, c2, end):
        t = _f32(t)
        start, c1, c2, end = _f32(start), _f32(c1), _f32(c2), _f32(end)
        return (start * (1.0 - t) * (1.0 - t) * (1.0 - t)
                + 3.0 * c1 * (1.0 - t) * (1.0 - t) * t
                + 3.0 * c2 * (1.0 - t) * t * t
                + end * t * t * t)
