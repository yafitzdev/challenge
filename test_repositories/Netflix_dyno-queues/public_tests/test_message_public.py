import pytest
from src.dyno_queues.message import Message

def test_default_constructor():
    msg = Message()
    assert msg.get_id() is None
    assert msg.get_payload() is None
    assert msg.get_timeout() == 0
    assert msg.get_priority() == 0
    assert msg.get_shard() is None

def test_parameterized_constructor():
    msg = Message("def", "data")
    assert msg.get_id() == "def"
    assert msg.get_payload() == "data"

def test_setters_and_getters():
    msg = Message()
    msg.set_id("uvw")
    msg.set_payload("payloadX")
    msg.set_timeout(12000)
    msg.set_priority(5)
    msg.set_shard("shardB")

    assert msg.get_id() == "uvw"
    assert msg.get_payload() == "payloadX"
    assert msg.get_timeout() == 12000
    assert msg.get_priority() == 5
    assert msg.get_shard() == "shardB"

def test_set_timeout_with_time_unit():
    msg = Message()
    msg.set_timeout(3, "minutes")
    assert msg.get_timeout() == 180000

def test_set_priority_too_low():
    msg = Message()
    with pytest.raises(ValueError):
        msg.set_priority(-5)

def test_set_priority_too_high():
    msg = Message()
    with pytest.raises(ValueError):
        msg.set_priority(150)

def test_set_priority_boundary_values():
    msg = Message()
    msg.set_priority(1)
    assert msg.get_priority() == 1
    msg.set_priority(98)
    assert msg.get_priority() == 98

def test_equals_and_hash_code():
    m1 = Message("idX", "payload3")
    m2 = Message("idX", "payload4")
    m3 = Message("idY", "payload3")
    m4 = Message(None, "payloadA")
    m5 = Message(None, "payloadB")

    assert m1 == m2
    assert hash(m1) == hash(m2)

    assert m1 != m3
    assert hash(m1) != hash(m3)

    assert m1 != None
    assert m1 != object()
    assert m1 == m1

    assert m4 == m5
    assert hash(m4) == hash(m5)

    assert m1 != m4
    assert m4 != m1

def test_to_string():
    msg = Message("idToString", "payloadTest")
    msg.set_priority(12)
    msg.set_timeout(999)
    s = str(msg)
    assert "idToString" in s
    assert "payloadTest" in s
    assert "priority=12" in s
    assert "timeout=999" in s