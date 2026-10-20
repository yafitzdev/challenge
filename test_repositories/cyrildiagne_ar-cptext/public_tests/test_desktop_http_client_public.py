import pytest
from src.arcopypaste.research.prototypes.text.DesktopHTTPClient import DesktopHTTPClient
from src.arcopypaste.research.prototypes.text.DesktopHTTPClientCallback import DesktopHTTPClientCallback

def test_get_absolute_url_with_different_suffix():
    method = getattr(DesktopHTTPClient, "_get_absolute_url")
    url = method("/public-data")
    assert url.endswith("/public-data") or "/public-data" in url

def test_set_different_position_and_no_crash():
    DesktopHTTPClient.setPosition(5.5, -3.3)

def test_set_text_with_different_input_and_no_crash():
    DesktopHTTPClient.setText("This is a public test string!")

def test_paste_and_no_crash_public():
    DesktopHTTPClient.paste()

def test_get_screenshot_returns_none_public(mocker):
    cb = mocker.Mock(spec=DesktopHTTPClientCallback)
    result = DesktopHTTPClient.getScreenshot(cb)
    assert result is None