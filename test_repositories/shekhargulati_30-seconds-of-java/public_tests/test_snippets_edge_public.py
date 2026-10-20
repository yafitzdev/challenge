import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from snippets import Snippets

def test_reverse_string_edge_public():
    assert Snippets.reverse_string("A") == "A"
    assert Snippets.reverse_string("AB") == "BA"

def test_is_palindrome_edge_public():
    assert Snippets.is_palindrome("a")
    assert Snippets.is_palindrome("")

def test_factorial_edge_public():
    assert Snippets.factorial(2) == 2
    assert Snippets.factorial(1) == 1