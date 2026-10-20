import pytest
from src.smsradar.shared_preferences_sms_storage import SharedPreferencesSmsStorage

class TestSharedPreferencesSmsStorage:
    DEFAULT_VALUE = -1
    ANY_SMS_ID = 1

    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.smsStorage = SharedPreferencesSmsStorage()
        yield
        self.smsStorage.clearPreferences()

    def test_should_return_default_value_if_not_edited_previously(self):
        assert self.smsStorage.getLastSmsIntercepted() == self.DEFAULT_VALUE

    def test_should_update_last_sms_intercepted_id(self):
        self.smsStorage.updateLastSmsIntercepted(self.ANY_SMS_ID)
        assert self.smsStorage.getLastSmsIntercepted() == self.ANY_SMS_ID

    def test_should_return_true_if_is_the_first_sms_intercepted(self):
        assert self.smsStorage.isFirstSmsIntercepted()