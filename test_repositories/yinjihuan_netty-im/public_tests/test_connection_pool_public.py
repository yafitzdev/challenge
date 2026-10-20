import pytest
from src.nettyim.connection_pool import ConnectionPool, ChannelHandlerContext

@pytest.fixture(autouse=True)
def clean_pool():
    ConnectionPool.clear()
    yield
    ConnectionPool.clear()

def test_put_and_get_channel_with_different_id():
    ctx = object()
    assert ConnectionPool.getChannel("public_id") is None
    ConnectionPool.putChannel("publicUserA", ctx)
    assert ConnectionPool.getChannel("publicUserA") is ctx

def test_put_channel_returns_old_value_public():
    ctx1 = object()
    ctx2 = object()
    assert ConnectionPool.putChannel("publicClient", ctx1) is None
    assert ConnectionPool.putChannel("publicClient", ctx2) is ctx1
    assert ConnectionPool.getChannel("publicClient") is ctx2

def test_get_channel_null_client_id_public():
    assert ConnectionPool.getChannel(None) is None

def test_get_clients_public():
    ctx = object()
    ConnectionPool.putChannel("alice", ctx)
    clients = ConnectionPool.getClients()
    assert "alice" in clients
    assert "bob" not in clients
    assert clients is not None

def test_get_channels_public():
    ctx4 = object()
    ConnectionPool.putChannel("publicFour", ctx4)
    channels = ConnectionPool.getChannels()
    assert ctx4 in channels
    assert len(ConnectionPool.getClients()) == len(channels)

def test_put_channel_null_client_id_public():
    ctx = object()
    assert ConnectionPool.putChannel(None, ctx) is None