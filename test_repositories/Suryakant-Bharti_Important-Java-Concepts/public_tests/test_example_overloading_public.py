from src.methodoverloading.example_overloading import ExampleOverloading

def test_min_function_int():
    assert ExampleOverloading.min_function(5, 2) == 2
    assert ExampleOverloading.min_function(-7, 9) == -7
    assert ExampleOverloading.min_function(-15, -20) == -20
    assert ExampleOverloading.min_function(0, 0) == 0

def test_min_function_double():
    assert abs(ExampleOverloading.min_function(8.7, 3.2) - 3.2) < 1e-9
    assert abs(ExampleOverloading.min_function(-9.8, 4.5) - (-9.8)) < 1e-9
    assert abs(ExampleOverloading.min_function(-11.3, -6.5) - (-11.3)) < 1e-9
    assert abs(ExampleOverloading.min_function(-7.7, -7.7) - (-7.7)) < 1e-9