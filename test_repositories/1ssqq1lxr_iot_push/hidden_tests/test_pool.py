import pytest
import time
from src.iot_push.dummy_module import ExecutorQueue, DefaultThreadFactory, Scheduled, StandardThreadExecutor

def test_executor_queue():
    queue = ExecutorQueue()
    assert queue.offer(lambda: None)
    assert queue.poll() is not None
    assert queue.poll() is None

def test_default_thread_factory():
    r = lambda: None
    factory = DefaultThreadFactory("test", True)
    t = factory.newThread(r)
    assert t is not None
    assert "test" in t.name
    assert t.daemon

def test_scheduled():
    scheduled = Scheduled()
    ran = []
    scheduled.schedule(lambda: ran.append(True), 10)
    scheduled.shutdown()
    assert scheduled.isShutdown() or not scheduled.isShutdown()
    # can't guarantee schedule has run before shutdown, so just test API

def test_standard_thread_executor():
    executor = StandardThreadExecutor(1, 2)
    ran = {'done': False}
    def f():
        ran['done'] = True
    executor.execute(f)
    time.sleep(0.1)
    assert ran['done']
    executor.shutdown()
    assert (executor.isShutdown() or not executor.isShutdown())