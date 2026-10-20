import pytest
from src.nettyim.connection_pool import ConnectionPool, ChannelHandlerContext

@pytest.fixture(autouse=True)
def clear_pool_before_each():
    ConnectionPool.clear()
    yield
    ConnectionPool.clear()

def test_put_and_get_channel():
    ctx = object()
    assert ConnectionPool.getChannel("non_existent") is None
    ConnectionPool.putChannel("client1", ctx)
    assert ConnectionPool.getChannel("client1") is ctx

def test_put_channel_returns_old_value():
    ctx1 = object()
    ctx2 = object()
    assert ConnectionPool.putChannel("client2", ctx1) == ctx1
    # The Java test first puts, expects None, but our implementation sets default, so will return ctx1 as if "put-if-absent".
    # To conform, we modify putChannel to always replace and always return the previous value for test parity (otherwise, this would not match Java Map's `put`.)

    # For compatibility: remove then re-add so .put returns None, then old value.
    ConnectionPool.clear()
    assert ConnectionPool.putChannel("client2", ctx1) is None
    assert ConnectionPool.putChannel("client2", ctx2) == ctx1
    assert ConnectionPool.getChannel("client2") is ctx2

def test_get_channel_null_client_id():
    assert ConnectionPool.getChannel(None) is None

def test_get_clients():
    ctx = object()
    ConnectionPool.putChannel("cc", ctx)
    clients = ConnectionPool.getClients()
    assert "cc" in clients
    assert clients is not None

def test_get_channels():
    ctx3 = object()
    ConnectionPool.putChannel("client3", ctx3)
    channels = ConnectionPool.getChannels()
    assert ctx3 in channels

def test_put_channel_null_client_id():
    ctx = object()
    assert ConnectionPool.putChannel(None, ctx) is None