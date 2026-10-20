import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))
from snippets import Snippets

def test_reverse_string_unicode():
    assert Snippets.reverse_string("こんにちは") == "はちにんこ"
    assert Snippets.reverse_string("123🙂") == "🙂321"

def test_is_palindrome_case():
    assert not Snippets.is_palindrome("Madam"), "Case sensitivity check"

def test_factorial_large():
    assert Snippets.factorial(10) == 3628800