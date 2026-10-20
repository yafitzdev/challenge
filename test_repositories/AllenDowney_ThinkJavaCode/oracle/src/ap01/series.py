"""Example method from Chapter 6 (port of ap01/Series.java)."""


class Series:

    @staticmethod
    def fibonacci(n):
        if n == 1 or n == 2:
            return 1
        return Series.fibonacci(n - 1) + Series.fibonacci(n - 2)

    @staticmethod
    def main(args):
        import sys
        if Series.fibonacci(1) != 1:
            print("fibonacci(1) is incorrect", file=sys.stderr)
        if Series.fibonacci(2) != 1:
            print("fibonacci(2) is incorrect", file=sys.stderr)
        if Series.fibonacci(3) != 2:
            print("fibonacci(3) is incorrect", file=sys.stderr)
