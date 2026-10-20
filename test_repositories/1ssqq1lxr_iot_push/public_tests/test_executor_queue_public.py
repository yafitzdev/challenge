import pytest
from src.iot_push.dummy_module import ExecutorQueue

def test_offer_and_poll_with_different_values():
    queue = ExecutorQueue()
    assert queue.offer(99)
    assert queue.poll() == 99
    assert queue.poll() is None

def test_multiple_operations_with_strings():
    queue = ExecutorQueue()
    assert queue.offer("X")
    assert queue.offer("Y")
    assert queue.poll() == "X"
    assert queue.poll() == "Y"
    assert queue.poll() is None

def test_size_is_empty_with_different_type():
    queue = ExecutorQueue()
    assert queue.isEmpty()
    queue.offer(7.7)
    assert not queue.isEmpty()
    assert queue.size() == 1
    queue.poll()
    assert queue.isEmpty()
    assert queue.size() == 0