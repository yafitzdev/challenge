import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))
from snippets import Snippets

def test_reverse_string():
    assert Snippets.reverse_string("hello") == "olleh"
    assert Snippets.reverse_string("") == ""
    assert Snippets.reverse_string("a") == "a"

def test_is_palindrome():
    assert Snippets.is_palindrome("madam")
    assert not Snippets.is_palindrome("python")
    assert Snippets.is_palindrome("")

def test_factorial():
    assert Snippets.factorial(5) == 120
    assert Snippets.factorial(0) == 1
    assert Snippets.factorial(1) == 1

def test_factorial_negative():
    try:
        Snippets.factorial(-1)
        assert False, "Expected ValueError for negative input"
    except ValueError:
        assert True