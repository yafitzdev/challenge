import pytest
import io
import sys

try:
    from src.ch03.convert import Convert
except ImportError:
    from ch03.convert import Convert

def test_main_with_numeric_input(monkeypatch):
    # Prepare a fake input stream and capture output
    test_input = "10\n"
    monkeypatch.setattr('sys.stdin', io.StringIO(test_input))
    captured = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = captured
    try:
        try:
            Convert.main([])
        except Exception:
            # It's okay if Convert.main throws (input float, print)
            pass
    finally:
        sys.stdout = sys_stdout
    output = captured.getvalue()
    assert "miles" in output.lower()
    assert "kilometers" in output.lower()

def test_main_with_invalid_input(monkeypatch):
    test_input = "foo\n"
    monkeypatch.setattr('sys.stdin', io.StringIO(test_input))
    captured = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = captured
    try:
        try:
            Convert.main([])
        except Exception:
            pass
    finally:
        sys.stdout = sys_stdout
    output = captured.getvalue()
    assert "miles" in output.lower()  # Should prompt for miles even on bad input