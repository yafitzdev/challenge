import pytest
from src.iot_push.dummy_module import ConnectionException, NoFindHandlerException

def test_connection_exception_throw():
    with pytest.raises(ConnectionException):
        raise ConnectionException("Connection error")

def test_no_find_handler_exception_throw():
    with pytest.raises(NoFindHandlerException):
        raise NoFindHandlerException("No handler found")