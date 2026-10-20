from src.methodoverloading.example_overloading import ExampleOverloading

def test_min_function_int():
    assert ExampleOverloading.min_function(11, 6) == 6
    assert ExampleOverloading.min_function(-3, 4) == -3
    assert ExampleOverloading.min_function(-5, -2) == -5
    assert ExampleOverloading.min_function(7, 7) == 7

def test_min_function_double():
    assert abs(ExampleOverloading.min_function(7.3, 9.4) - 7.3) < 1e-9
    assert abs(ExampleOverloading.min_function(-5.5, 0.0) - (-5.5)) < 1e-9
    assert abs(ExampleOverloading.min_function(-10.2, -2.3) - (-10.2)) < 1e-9
    assert abs(ExampleOverloading.min_function(12.0, 12.0) - 12.0) < 1e-9