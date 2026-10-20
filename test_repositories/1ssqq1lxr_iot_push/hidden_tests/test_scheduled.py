import pytest
from src.iot_push.dummy_module import Scheduled

def test_scheduled_runnable():
    delay = 1000
    called = []
    def task():
        called.append(True)
    scheduled = Scheduled(task, delay)
    assert scheduled.getDelay() == delay
    scheduled.setDelay(500)
    assert scheduled.getDelay() == 500
    scheduled.shutdown()