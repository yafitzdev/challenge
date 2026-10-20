from src.methodoverloading.adder import Adder

def test_add_int():
    assert Adder.add(11, 11) == 22
    assert Adder.add(-10, 2) == -8
    assert Adder.add(0, 0) == 0

def test_add_double():
    assert abs(Adder.add(12.3, 12.6) - 24.9) < 1e-9
    assert abs(Adder.add(-2.2, -2.2) - (-4.4)) < 1e-9
    assert abs(Adder.add(0.0, 0.0) - 0.0) < 1e-9