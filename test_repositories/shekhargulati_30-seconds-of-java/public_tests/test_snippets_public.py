import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from snippets import Snippets

def test_reverse_string_public():
    assert Snippets.reverse_string("openai") == "ianepo"
    assert Snippets.reverse_string("abcde") == "edcba"

def test_is_palindrome_public():
    assert Snippets.is_palindrome("level")
    assert not Snippets.is_palindrome("levels")

def test_factorial_public():
    assert Snippets.factorial(3) == 6