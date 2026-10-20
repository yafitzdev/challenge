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
    msg = Message("abc", "payload")
    assert msg.get_id() == "abc"
    assert msg.get_payload() == "payload"

def test_setters_and_getters():
    msg = Message()
    msg.set_id("xyz")
    msg.set_payload("p1")
    msg.set_timeout(5000)
    msg.set_priority(10)
    msg.set_shard("shardA")

    assert msg.get_id() == "xyz"
    assert msg.get_payload() == "p1"
    assert msg.get_timeout() == 5000
    assert msg.get_priority() == 10
    assert msg.get_shard() == "shardA"

def test_set_timeout_with_time_unit():
    msg = Message()
    msg.set_timeout(2, "seconds")
    assert msg.get_timeout() == 2000

def test_set_priority_too_low():
    msg = Message()
    with pytest.raises(ValueError):
        msg.set_priority(-1)

def test_set_priority_too_high():
    msg = Message()
    with pytest.raises(ValueError):
        msg.set_priority(100)

def test_set_priority_boundary_values():
    msg = Message()
    msg.set_priority(0)
    assert msg.get_priority() == 0
    msg.set_priority(99)
    assert msg.get_priority() == 99

def test_equals_and_hash_code():
    m1 = Message("id1", "payload1")
    m2 = Message("id1", "payload2")
    m3 = Message("id2", "payload1")
    m4 = Message(None, "payload3")
    m5 = Message(None, "payload4")

    assert m1 == m2
    assert hash(m1) == hash(m2)
    assert m1 != m3
    assert hash(m1) != hash(m3)

    assert m1 != None
    assert m1 != "string"
    assert m1 == m1

    assert m4 == m5
    assert hash(m4) == hash(m5)

    assert m1 != m4
    assert m4 != m1

def test_to_string():
    msg = Message("idToStr", "payloadStr")
    msg.set_priority(7)
    msg.set_timeout(123)
    s = str(msg)
    assert "idToStr" in s
    assert "payloadStr" in s
    assert "priority=7" in s
    assert "timeout=123" in s