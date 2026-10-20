import pytest
import threading
from src.iot_push.dummy_module import DefaultThreadFactory

def test_new_thread_public():
    factory = DefaultThreadFactory("public-thread")
    thread_ref = []
    def r():
        thread_ref.append(threading.current_thread())
    t = factory.newThread(r)
    t.start()
    t.join()
    assert thread_ref
    assert "public-thread" in thread_ref[0].name