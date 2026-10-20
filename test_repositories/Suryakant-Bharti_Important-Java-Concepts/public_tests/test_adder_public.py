from src.methodoverloading.adder import Adder

def test_add_int():
    assert Adder.add(9, 8) == 17
    assert Adder.add(15, 10) == 25
    assert Adder.add(-3, -3) == -6

def test_add_double():
    assert abs(Adder.add(9.5, 11.6) - 21.1) < 1e-9
    assert abs(Adder.add(-7.7, 7.7) - 0.0) < 1e-9
    assert abs(Adder.add(-2.2, -4.4) - (-6.6)) < 1e-9