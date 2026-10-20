from src.nettyim.http import NettyHttpServer, NettyHttpServerHandler

def test_server_instantiation_public():
    server = NettyHttpServer()
    assert server is not None
    assert server.__class__.__name__.startswith("NettyHttpServer")

def test_handler_instantiation_public():
    handler = NettyHttpServerHandler()
    assert handler is not None
    assert "Handler" in handler.__class__.__name__