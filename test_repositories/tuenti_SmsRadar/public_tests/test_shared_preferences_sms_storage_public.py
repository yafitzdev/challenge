from src.smsradar.shared_preferences_sms_storage import SharedPreferencesSmsStorage

def test_put_and_get_value():
    storage = SharedPreferencesSmsStorage()
    storage.clearPreferences()
    storage.putString("animal", "dog")
    assert storage.getString("animal", "") == "dog"

def test_overwrite_value():
    storage = SharedPreferencesSmsStorage()
    storage.putString("language", "Python")
    storage.putString("language", "Go")
    assert storage.getString("language", "") == "Go"

def test_get_default_if_not_present():
    storage = SharedPreferencesSmsStorage()
    assert storage.getString("missing-key", "default") == "default"