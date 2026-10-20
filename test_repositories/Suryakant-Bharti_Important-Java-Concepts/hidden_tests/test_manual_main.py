import io
import sys
from src.methodoverloading.adder import Adder
from src.methodoverloading.example_overloading import ExampleOverloading
from src.methodoverloading.overloading_calculation2 import OverloadingCalculation2

def test_adder_main_manual():
    # Simulating Adder main usage (TestOverloading2.main just called Adder.add)
    assert Adder.add(11, 11) == 22
    assert abs(Adder.add(12.3, 12.6) - 24.9) < 1e-9

def test_example_overloading_main_manual():
    captured_output = io.StringIO()
    sys_stdout = sys.stdout
    try:
        sys.stdout = captured_output
        ExampleOverloading.main([])
    finally:
        sys.stdout = sys_stdout

    output = captured_output.getvalue()
    assert "Minimum Value = 6" in output
    assert "Minimum Value = 7.3" in output

def test_overloading_calculation2_main():
    captured_output = io.StringIO()
    sys_stdout = sys.stdout
    try:
        sys.stdout = captured_output
        OverloadingCalculation2.main([])
        sys.stdout = sys_stdout
        output = captured_output.getvalue()
        assert "int arg method invoked" in output
    finally:
        sys.stdout = sys_stdout