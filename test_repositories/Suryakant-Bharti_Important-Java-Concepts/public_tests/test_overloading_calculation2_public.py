import io
import sys
from src.methodoverloading.overloading_calculation2 import OverloadingCalculation2

def test_sum_int_args():
    obj = OverloadingCalculation2()
    captured_output = io.StringIO()
    sys_stdout = sys.stdout
    try:
        sys.stdout = captured_output
        obj.sum(8, 13)
        sys.stdout = sys_stdout
        assert "int arg method invoked" in captured_output.getvalue().strip()
    finally:
        sys.stdout = sys_stdout

def test_sum_long_args():
    obj = OverloadingCalculation2()
    captured_output = io.StringIO()
    sys_stdout = sys.stdout
    try:
        sys.stdout = captured_output
        obj.sum(13.0, 22.0)
        sys.stdout = sys_stdout
        assert "long arg method invoked" in captured_output.getvalue().strip()
    finally:
        sys.stdout = sys_stdout