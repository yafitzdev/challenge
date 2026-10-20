import pytest
from src.bluetoothlegatt.device_control_activity import DeviceControlActivity

def test_extras_constants_are_not_null():
    assert DeviceControlActivity.EXTRAS_DEVICE_NAME is not None
    assert DeviceControlActivity.EXTRAS_DEVICE_ADDRESS is not None