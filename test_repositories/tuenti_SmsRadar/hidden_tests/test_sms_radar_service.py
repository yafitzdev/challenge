import pytest
from src.smsradar.sms_radar_service import SmsRadarService

def test_service_can_be_constructed():
    service = SmsRadarService()
    assert service is not None