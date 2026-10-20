import pytest

from src.dyno_queues.message import Message

def test_timeout():
    msg = Message()
    msg.set_payload("payload")
    msg.set_timeout(10, "seconds")
    assert msg.get_timeout() == 10 * 1000
    msg.set_timeout(10)
    assert msg.get_timeout() == 10

def test_priority_negative():
    msg = Message()
    with pytest.raises(ValueError):
        msg.set_priority(-1)

def test_priority_too_large():
    msg = Message()
    with pytest.raises(ValueError):
        msg.set_priority(100)