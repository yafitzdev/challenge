import pytest
from src.iot_push.dummy_module import IpUtils

def test_host_ip_is_consistent_with_inet_address():
    host_ip = IpUtils.getHostIp()
    assert host_ip is not None
    assert host_ip.strip() != ""
    assert host_ip != "0.0.0.0"