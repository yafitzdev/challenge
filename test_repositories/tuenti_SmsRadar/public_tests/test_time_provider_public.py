import time
from src.smsradar.time_provider import TimeProvider

def test_epoch_time():
    tp = TimeProvider()
    t = tp.getCurrentTimeMillis()
    assert t >= 0

def test_time_has_advanced():
    tp = TimeProvider()
    before = tp.getCurrentTimeMillis()
    time.sleep(0.007)
    after = tp.getCurrentTimeMillis()
    assert after > before