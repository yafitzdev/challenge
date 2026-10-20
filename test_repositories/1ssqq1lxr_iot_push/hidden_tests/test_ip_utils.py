import pytest
from src.iot_push.dummy_module import IpUtils

def test_localhost_address():
    ip = IpUtils.getHostIp()
    assert ip is not None
    assert ip != ""