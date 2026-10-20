import pytest
import io
import sys

try:
    from src.ch01.hello import Hello
except ImportError:
    from ch01.hello import Hello

def test_hello_main_output_different_data(monkeypatch):
    captured = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = captured
    try:
        Hello.main([])
    finally:
        sys.stdout = sys_stdout
    output = captured.getvalue().strip()
    assert output.startswith("Hello") or "Hello" in output
    assert "Goodbye" in output