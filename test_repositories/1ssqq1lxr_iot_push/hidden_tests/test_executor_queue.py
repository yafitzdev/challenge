import pytest
from src.iot_push.dummy_module import ExecutorQueue

def test_offer_and_poll():
    queue = ExecutorQueue()
    assert queue.offer(1)
    assert queue.poll() == 1
    assert queue.poll() is None

def test_multiple_operations():
    queue = ExecutorQueue()
    assert queue.offer("A")
    assert queue.offer("B")
    assert queue.poll() == "A"
    assert queue.poll() == "B"
    assert queue.poll() is None

def test_size_is_empty():
    queue = ExecutorQueue()
    assert queue.isEmpty()
    queue.offer(2.5)
    assert not queue.isEmpty()
    assert queue.size() == 1
    queue.poll()
    assert queue.isEmpty()
    assert queue.size() == 0