import io
import sys
import pytest
from src.methodoverloading.overloading_calculation2 import OverloadingCalculation2

class TestOverloadingCalculation2:
    def test_sum_int_args(self):
        obj = OverloadingCalculation2()
        captured_output = io.StringIO()
        sys_stdout = sys.stdout
        try:
            sys.stdout = captured_output
            obj.sum(1, 2)
            sys.stdout = sys_stdout
            assert "int arg method invoked" in captured_output.getvalue().strip()
        finally:
            sys.stdout = sys_stdout

    def test_sum_long_args(self):
        obj = OverloadingCalculation2()
        captured_output = io.StringIO()
        sys_stdout = sys.stdout
        try:
            sys.stdout = captured_output
            # Python can't distinguish long, but simulate with floats.
            obj.sum(5.0, 6.0)
            sys.stdout = sys_stdout
            assert "long arg method invoked" in captured_output.getvalue().strip()
        finally:
            sys.stdout = sys_stdout