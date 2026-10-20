from src.nettyim.handler import ServerPoHandler, ServerPoHandlerProto, ServerStringHandler

def test_server_po_handler_construction_public():
    handler = ServerPoHandler()
    assert handler is not None
    assert handler.__class__.__name__ == "ServerPoHandler"

def test_server_po_handler_proto_construction_public():
    handler_proto = ServerPoHandlerProto()
    assert handler_proto is not None
    assert "Proto" in handler_proto.__class__.__name__

def test_server_string_handler_construction_public():
    string_handler = ServerStringHandler()
    assert string_handler is not None
    assert "String" in string_handler.__class__.__name__