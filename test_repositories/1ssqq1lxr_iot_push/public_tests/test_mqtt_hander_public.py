import pytest
from src.iot_push.dummy_module import MqttHander

def test_instantiation():
    hander = MqttHander()
    assert hander is not None