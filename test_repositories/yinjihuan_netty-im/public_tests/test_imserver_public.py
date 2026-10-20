from src.nettyim.server import ImServer

def test_im_server_constructor_public():
    server = ImServer()
    assert server.__class__.__name__ == "ImServer"