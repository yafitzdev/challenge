from src.nettyim.handler import ServerPoHandler
import pytest

class DummyCtx:
    def __init__(self):
        self._written = []

    def write_and_flush(self, msg):
        self._written.append(msg)

    def get_written(self):
        return self._written

def test_channel_read_basic():
    ctx = DummyCtx()
    handler = ServerPoHandler()
    handler.channelRead(ctx, "hello")
    assert "hello" in ctx.get_written()

def test_channel_read_null_msg():
    ctx = DummyCtx()
    handler = ServerPoHandler()
    handler.channelRead(ctx, None)
    # Should handle null message gracefully (shouldn't throw, and nothing added)
    assert ctx.get_written() == []