"""Partial port of snippets.Snippets (the string helpers exercised by the tests).

Note: the Java Snippets class has no factorial method, so none is provided here.
"""
import re

_NON_WORD = re.compile(r"[\W_]", re.ASCII)


class Snippets:

    @staticmethod
    def is_palindrome(input):
        # Java: input.toLowerCase().replaceAll("[\\W_]", "") then compare with reverse
        s = _NON_WORD.sub("", input.lower())
        return s == s[::-1]

    @staticmethod
    def reverse_string(input):
        # Java StringBuilder.reverse keeps surrogate pairs intact, i.e. reverses code points.
        return input[::-1]

    isPalindrome = is_palindrome
    reverseString = reverse_string
