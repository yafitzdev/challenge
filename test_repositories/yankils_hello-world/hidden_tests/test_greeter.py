import pytest
from src.greeter import Greeter

class TestGreeter:

    def test_greet_normal(self):
        greeter = Greeter()
        result = greeter.greet("World")
        assert result == "Hello, World!"

    def test_greet_empty(self):
        greeter = Greeter()
        result = greeter.greet("")
        assert result == "Hello, !"

    def test_greet_whitespace(self):
        greeter = Greeter()
        result = greeter.greet("   ")
        assert result == "Hello,    !"

    def test_greet_null(self):
        greeter = Greeter()
        # In Python, passing None will result in a string "None"
        result = greeter.greet(None)
        assert result == "Hello, None!"

    def test_greet_custom_name(self):
        greeter = Greeter()
        result = greeter.greet("Alice")
        assert result == "Hello, Alice!"