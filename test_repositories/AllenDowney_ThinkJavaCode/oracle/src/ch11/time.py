"""Represents a time of day (port of ch11/Time.java)."""


class Time:

    def __init__(self, hour=0, minute=0, second=0.0):
        self.hour = hour
        self.minute = minute
        self.second = float(second)

    @staticmethod
    def print_time(t):
        print(t.hour, end="")
        print(":", end="")
        print(t.minute)
        print(":", end="")
        print(repr(float(t.second)))

    def __str__(self):
        return "%02d:%02d:%04.1f\n" % (self.hour, self.minute, self.second)

    to_string = __str__

    def equals(self, that):
        return (self.hour == that.hour
                and self.minute == that.minute
                and self.second == that.second)

    def __eq__(self, other):
        if not isinstance(other, Time):
            return NotImplemented
        return self.equals(other)

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    __hash__ = object.__hash__

    @staticmethod
    def _add_static(t1, t2):
        total = Time()
        total.hour = t1.hour + t2.hour
        total.minute = t1.minute + t2.minute
        total.second = t1.second + t2.second
        return total

    def _add_instance(self, t2):
        total = Time()
        total.hour = self.hour + t2.hour
        total.minute = self.minute + t2.minute
        total.second = self.second + t2.second
        if total.second >= 60.0:
            total.second -= 60.0
            total.minute += 1
        if total.minute >= 60:
            total.minute -= 60
            total.hour += 1
        return total

    def increment(self, seconds):
        self.second += seconds
        while self.second >= 60.0:
            self.second -= 60.0
            self.minute += 1
        while self.minute >= 60:
            self.minute -= 60
            self.hour += 1


class _AddDescriptor:
    """Java overloads add(Time, Time) (static) and add(Time) (instance)."""

    def __get__(self, obj, objtype=None):
        if obj is None:
            return Time._add_static
        return obj._add_instance


Time.add = _AddDescriptor()
