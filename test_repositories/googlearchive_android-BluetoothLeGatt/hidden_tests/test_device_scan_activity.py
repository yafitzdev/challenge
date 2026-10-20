import pytest
from src.bluetoothlegatt.device_scan_activity import DeviceScanActivity

def test_scan_period_is_10000():
    assert DeviceScanActivity.SCAN_PERIOD == 10000