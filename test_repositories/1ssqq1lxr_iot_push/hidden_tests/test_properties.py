import pytest
from src.iot_push.dummy_module import MqttProperties

def test_mqtt_properties():
    props = MqttProperties()
    props.setPort(1883)
    props.setHost("127.0.0.1")
    props.setClientId("cid")
    props.setUsername("user")
    props.setPassword("pass")
    props.setCleanSession(True)
    props.setKeepalive(120)
    props.setQos(1)

    assert props.getPort() == 1883
    assert props.getHost() == "127.0.0.1"
    assert props.getClientId() == "cid"
    assert props.getUsername() == "user"
    assert props.getPassword() == "pass"
    assert props.isCleanSession() == True
    assert props.getKeepalive() == 120
    assert props.getQos() == 1