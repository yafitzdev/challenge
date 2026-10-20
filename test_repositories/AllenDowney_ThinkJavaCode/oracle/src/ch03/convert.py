"""Converts centimeters to feet and inches (port of ch03/Convert.java)."""
import sys


class _Scanner:
    """Minimal java.util.Scanner replacement reading whitespace tokens."""

    def __init__(self, stream):
        self._stream = stream
        self._tokens = []

    def _next(self):
        while not self._tokens:
            line = self._stream.readline()
            if line == "":
                raise EOFError("NoSuchElementException")
            self._tokens = line.split()
        return self._tokens.pop(0)

    def next_double(self):
        tok = self._next()
        try:
            return float(tok)
        except ValueError:
            self._tokens.insert(0, tok)
            raise ValueError("InputMismatchException: " + tok)


class Convert:

    @staticmethod
    def main(args):
        CM_PER_INCH = 2.54
        IN_PER_FOOT = 12
        scanner = _Scanner(sys.stdin)

        # prompt the user and get the value
        print("Exactly how many cm? ", end="")
        cm = scanner.next_double()

        # convert and output the result
        inches = int(cm / CM_PER_INCH)
        feet = inches // IN_PER_FOOT
        remainder = inches % IN_PER_FOOT
        print("%.2f cm = %d ft, %d in" % (cm, feet, remainder))
