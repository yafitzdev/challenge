import pytest
from src.iot_push.dummy_module import ServerMqttHandlerService

def test_server_mqtt_handler_construction():
    s = ServerMqttHandlerService()
    assert s is not None