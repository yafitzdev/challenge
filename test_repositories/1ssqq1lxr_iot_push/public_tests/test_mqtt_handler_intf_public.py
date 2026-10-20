import pytest
from src.iot_push.dummy_module import MqttHandlerIntf

def test_interface_public_impl():
    class PublicDummyMqttHandler(MqttHandlerIntf): pass
    PublicDummyMqttHandler()