import pytest
from src.iot_push.dummy_module import ConfirmStatus, ProtocolEnum, QosStatus, SessionStatus, SubStatus

def test_confirm_status_enum():
    values = list(ConfirmStatus)
    assert len(values) == 2
    assert ConfirmStatus.PUBLISH.name == "PUBLISH"
    assert ConfirmStatus.PUBREL.name == "PUBREL"

def test_protocol_enum():
    values = list(ProtocolEnum)
    assert len(values) == 2
    assert ProtocolEnum.MQTT.name == "MQTT"
    assert ProtocolEnum.WEBSOCKET.name == "WEBSOCKET"

def test_qos_status():
    values = list(QosStatus)
    assert len(values) == 3
    assert QosStatus.QOS0.name == "QOS0"
    assert QosStatus.QOS1.name == "QOS1"
    assert QosStatus.QOS2.name == "QOS2"
    assert QosStatus.QOS0.value == 0
    assert QosStatus.QOS1.value == 1
    assert QosStatus.QOS2.value == 2

def test_session_status():
    values = list(SessionStatus)
    assert len(values) == 2
    assert SessionStatus.CLOSE.name == "CLOSE"
    assert SessionStatus.OPEN.name == "OPEN"

def test_sub_status():
    values = list(SubStatus)
    assert len(values) == 2
    assert SubStatus.CANCEL.name == "CANCEL"
    assert SubStatus.SUBSCRIBE.name == "SUBSCRIBE"