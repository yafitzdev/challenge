import pytest
from src.iot_push.dummy_module import ClientMqttHandlerService

def test_client_mqtt_handler_construction():
    c = ClientMqttHandlerService()
    assert c is not None