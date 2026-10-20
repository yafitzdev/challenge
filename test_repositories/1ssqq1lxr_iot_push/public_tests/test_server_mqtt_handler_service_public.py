import pytest
from src.iot_push.dummy_module import ServerMqttHandlerService

def test_server_mqtt_handler_new_construction():
    class PubServer(ServerMqttHandlerService):
        pass
    server = PubServer()
    assert server is not None