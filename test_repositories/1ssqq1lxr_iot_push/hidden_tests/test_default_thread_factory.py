import pytest
import threading
from src.iot_push.dummy_module import DefaultThreadFactory

def test_new_thread():
    factory = DefaultThreadFactory("test")
    thread_ref = []
    def r():
        thread_ref.append(threading.current_thread())
    t = factory.newThread(r)
    t.start()
    t.join()
    assert thread_ref
    assert thread_ref[0].name.startswith("test-")