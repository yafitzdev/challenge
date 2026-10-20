import pytest
import io
import sys

try:
    from src.ch01.hello import Hello
    from src.ch01.goodbye import Goodbye
except ImportError:
    try:
        from ch01.hello import Hello
        from ch01.goodbye import Goodbye
    except ImportError:
        Hello = None
        Goodbye = None

def test_hello_output(monkeypatch):
    if Hello is None:
        pytest.skip("Hello class not implemented or importable")
    captured = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = captured
    try:
        Hello.main([])
    finally:
        sys.stdout = sys_stdout
    output = captured.getvalue().strip()
    assert output == "Hello, World!"

def test_goodbye_output(monkeypatch):
    if Goodbye is None:
        pytest.skip("Goodbye class not implemented or importable")
    captured = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = captured
    try:
        Goodbye.main([])
    finally:
        sys.stdout = sys_stdout
    output = captured.getvalue().replace("\r", "").strip()
    assert output == "Goodbye, cruel world"