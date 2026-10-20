import pytest
from src.arcopypaste.research.prototypes.text.DesktopHTTPClient import DesktopHTTPClient
from src.arcopypaste.research.prototypes.text.DesktopHTTPClientCallback import DesktopHTTPClientCallback

def test_get_absolute_url_reflect():
    method = getattr(DesktopHTTPClient, "_get_absolute_url")
    url = method("/test")
    assert "/test" in url

def test_set_position_and_no_crash():
    DesktopHTTPClient.setPosition(1.0, 2.0)

def test_set_text_and_no_crash():
    DesktopHTTPClient.setText("Hello World")

def test_paste_and_no_crash():
    DesktopHTTPClient.paste()

def test_get_screenshot_returns_none(mocker):
    cb = mocker.Mock(spec=DesktopHTTPClientCallback)
    result = DesktopHTTPClient.getScreenshot(cb)
    assert result is None