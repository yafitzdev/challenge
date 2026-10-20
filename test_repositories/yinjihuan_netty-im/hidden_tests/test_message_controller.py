from src.nettyim.controller import MessageController
from src.nettyim.connection_pool import ConnectionPool

class DummyCtx:
    def __init__(self):
        self._written = []

    def write_and_flush(self, msg):
        self._written.append(msg)

    def get_written(self):
        return self._written

def setup_function(function):
    ConnectionPool.clear()

def test_push_all_message():
    ctx1 = DummyCtx()
    ConnectionPool.putChannel("A", ctx1)
    controller = MessageController()
    result = controller.pushAllMessage("HelloAll")
    assert result == "success"
    assert "HelloAll" in ctx1.get_written()

def test_push_message_to_client():
    ctx = DummyCtx()
    ConnectionPool.putChannel("uniqueID", ctx)
    controller = MessageController()
    result = controller.pushAllMessage("uniqueID", "HiGuy")
    assert result == "success"
    assert "HiGuy" in ctx.get_written()

def test_push_message_to_client_not_found():
    controller = MessageController()
    result = controller.pushAllMessage("non-existent", "msg")
    assert result == "success"