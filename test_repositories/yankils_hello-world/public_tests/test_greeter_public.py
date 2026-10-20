import pytest
from src.greeter import Greeter

class TestGreeterPublic:

    def test_greet_another_name(self):
        greeter = Greeter()
        result = greeter.greet("Alice")
        assert result == "Hello, Alice!"

    def test_greet_with_different_name(self):
        greeter = Greeter()
        result = greeter.greet("Charlie")
        assert result == "Hello, Charlie!"

    def test_greet_with_empty_string(self):
        greeter = Greeter()
        result = greeter.greet("")
        assert result == "Hello, !"

    def test_greet_with_special_characters(self):
        greeter = Greeter()
        result = greeter.greet("@User#123")
        assert result == "Hello, @User#123!"