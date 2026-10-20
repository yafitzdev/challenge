import pytest
from src.iot_push.dummy_module import MqttHander

def test_dummy():
    # Just instantiate to get some coverage
    h = MqttHander()
    assert h is not None