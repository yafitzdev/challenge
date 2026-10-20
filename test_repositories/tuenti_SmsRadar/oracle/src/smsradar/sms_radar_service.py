"""Port of com.tuenti.smsradar.SmsRadarService (an android Service).

Android framework collaborators (ContentResolver, AlarmManager, SharedPreferences, Handler) are
injected through the setters, mirroring the package-private setters of the Java class.
"""
from .shared_preferences_sms_storage import SharedPreferencesSmsStorage
from .sms_cursor_parser import SmsCursorParser
from .sms_observer import SmsObserver
from .time_provider import TimeProvider


class SmsRadarService(object):
    CONTENT_SMS_URI = "content://sms"
    ONE_SECOND = 1000
    START_STICKY = 1
    RTC_WAKEUP = 0

    def __init__(self):
        self._content_resolver = None
        self._sms_observer = None
        self._alarm_manager = None
        self._time_provider = None
        self._initialized = False
        self._shared_preferences = None
        self._system_content_resolver = None

    def onBind(self, intent):
        return None

    def onStartCommand(self, intent, flags, start_id):
        if not self._initialized:
            self._initialize_service()
        return self.START_STICKY

    def onDestroy(self):
        self._finish_service()

    def onTaskRemoved(self, root_intent):
        self._restart_service()

    def _initialize_service(self):
        self._initialized = True
        self._initialize_dependencies()
        self._register_sms_content_observer()

    def _initialize_dependencies(self):
        if not (self._content_resolver is not None and self._sms_observer is not None):
            self._content_resolver = self.getContentResolver()
            self._sms_observer = SmsObserver(self._content_resolver, None,
                                             self._initialize_sms_cursor_parser())

    def _initialize_sms_cursor_parser(self):
        storage = SharedPreferencesSmsStorage(self.getSharedPreferences("sms_preferences"))
        return SmsCursorParser(storage, self._get_time_provider())

    def _finish_service(self):
        self._initialized = False
        self._content_resolver.unregisterContentObserver(self._sms_observer)

    def _register_sms_content_observer(self):
        self._content_resolver.registerContentObserver(self.CONTENT_SMS_URI, True, self._sms_observer)

    def _restart_service(self):
        date = self._get_time_provider().getDate()
        now = date.getTime() if hasattr(date, "getTime") else int(date.timestamp() * 1000)
        self._get_alarm_manager().set(self.RTC_WAKEUP, now + self.ONE_SECOND, SmsRadarService)

    def _get_time_provider(self):
        return self._time_provider if self._time_provider is not None else TimeProvider()

    def _get_alarm_manager(self):
        return self._alarm_manager

    # Android context hooks (overridable).
    def getContentResolver(self):
        return self._system_content_resolver

    def getSharedPreferences(self, name):
        return self._shared_preferences

    def setSmsObserver(self, sms_observer):
        self._sms_observer = sms_observer

    def setContentResolver(self, content_resolver):
        self._content_resolver = content_resolver

    def setAlarmManager(self, alarm_manager):
        self._alarm_manager = alarm_manager

    def setTimeProvider(self, time_provider):
        self._time_provider = time_provider
