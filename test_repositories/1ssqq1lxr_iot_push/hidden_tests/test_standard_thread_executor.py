import pytest
from src.iot_push.dummy_module import StandardThreadExecutor

def test_execute_and_shutdown():
    executor = StandardThreadExecutor(1, 2, 1000)
    def task():
        return "executed"
    future = executor.submit(task)
    assert future.get() == "executed"
    executor.shutdown()
    assert (executor.isShutdown() or executor.isTerminated())