import pytest
from src.iot_push.dummy_module import MqttHandlerIntf

def test_mqtt_handler_intf_impl():
    class DummyMqttHandler(MqttHandlerIntf):
        pass
    d = DummyMqttHandler()
    assert isinstance(d, MqttHandlerIntf)