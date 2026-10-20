import pytest

try:
    from src.ch03.convert import Convert
except ImportError:
    from ch03.convert import Convert

def test_celsius_to_fahrenheit_public_data():
    assert abs(Convert.celsius_to_fahrenheit(0) - 32.0) < 0.01
    assert abs(Convert.celsius_to_fahrenheit(50) - 122.0) < 0.01
    assert abs(Convert.celsius_to_fahrenheit(20) - 68.0) < 0.01
    assert abs(Convert.celsius_to_fahrenheit(37) - 98.6) < 0.01

def test_fahrenheit_to_celsius_public_data():
    assert abs(Convert.fahrenheit_to_celsius(32) - 0.0) < 0.01
    assert abs(Convert.fahrenheit_to_celsius(212) - 100.0) < 0.01
    assert abs(Convert.fahrenheit_to_celsius(104) - 40.0) < 0.01
    assert abs(Convert.fahrenheit_to_celsius(41) - 5.0) < 0.01