import pytest

try:
    from src.ch11.time_client import TimeClient
except ImportError:
    from ch11.time_client import TimeClient

def test_smoke_test_main(monkeypatch):
    # Just runs main, should not throw
    TimeClient.main([])