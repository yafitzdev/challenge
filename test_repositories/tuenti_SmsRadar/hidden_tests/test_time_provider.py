import time
from src.smsradar.time_provider import TimeProvider

def test_get_date_returns_now():
    provider = TimeProvider()
    before = int(time.time() * 1000)
    dt = provider.getDate()
    after = int(time.time() * 1000)
    assert dt is not None
    # dt is a datetime, convert to millis:
    assert before <= int(dt.timestamp() * 1000) <= after

def test_now_returns_current_time():
    provider = TimeProvider()
    before = int(time.time() * 1000)
    now = provider.now()
    after = int(time.time() * 1000)
    assert before <= now <= after

def test_get_current_time_millis_public():
    tp = TimeProvider()
    t = tp.getCurrentTimeMillis()
    assert t >= 0

def test_time_advancing_public():
    tp = TimeProvider()
    before = tp.getCurrentTimeMillis()
    time.sleep(0.008)
    after = tp.getCurrentTimeMillis()
    assert after > before