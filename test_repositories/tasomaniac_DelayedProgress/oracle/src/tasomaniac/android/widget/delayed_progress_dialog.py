"""Python port of com.tasomaniac.android.widget.DelayedProgressDialog."""
from ._handler import Handler, now_millis


class DelayedProgressDialog:

    def __init__(self, context, theme_res_id=None):
        self._context = context
        self._theme = theme_res_id
        self._title = None
        self._message = None
        self._indeterminate = False
        self._cancelable = True
        self._on_cancel_listener = None
        self._is_showing = False
        self._start_time = -1
        self._posted_hide = False
        self._posted_show = False
        self._dismissed = False
        self._min_show_time = 500  # ms
        self._min_delay = 500  # ms
        self._handler = Handler()

    # ---- showing state: setting it True mirrors the delayed show firing,
    # setting it False mirrors the delayed hide firing ----
    @property
    def _showing(self):
        return self._is_showing

    @_showing.setter
    def _showing(self, value):
        if value:
            self._delayed_show()
        else:
            self._delayed_hide()

    # ---- ProgressDialog-like API ----
    def setTitle(self, title):
        self._title = title

    def setMessage(self, message):
        self._message = message

    def setIndeterminate(self, indeterminate):
        self._indeterminate = indeterminate

    def setCancelable(self, cancelable):
        self._cancelable = cancelable

    def setOnCancelListener(self, listener):
        self._on_cancel_listener = listener

    def isShowing(self):
        return self._is_showing

    def _super_show(self):
        self._is_showing = True

    def _super_dismiss(self):
        self._is_showing = False

    def setMinShowTime(self, min_show_time):
        self._min_show_time = min_show_time

    def setMinDelay(self, min_delay):
        self._min_delay = min_delay

    # ---- runnables ----
    def _delayed_hide(self):
        self._posted_hide = False
        self._start_time = -1
        self._super_dismiss()

    def _delayed_show(self):
        self._posted_show = False
        if not self._dismissed:
            self._start_time = now_millis()
            self._super_show()

    # ---- factories ----
    @staticmethod
    def make(context, title, message, indeterminate=False, cancelable=False,
             cancel_listener=None):
        dialog = DelayedProgressDialog(context)
        dialog.setTitle(title)
        dialog.setMessage(message)
        dialog.setIndeterminate(indeterminate)
        dialog.setCancelable(cancelable)
        dialog.setOnCancelListener(cancel_listener)
        return dialog

    @staticmethod
    def showDelayed(context, title, message, indeterminate=False, cancelable=False,
                    cancel_listener=None):
        dialog = DelayedProgressDialog.make(context, title, message, indeterminate,
                                            cancelable, cancel_listener)
        dialog.show()
        return dialog

    def onDetachedFromWindow(self):
        self._remove_callbacks()

    def _remove_callbacks(self):
        if self._handler is not None:
            self._handler.remove_callbacks(self._delayed_hide)
            self._posted_hide = False
            self._handler.remove_callbacks(self._delayed_show)
            self._posted_show = False

    def dismiss(self):
        self._dismissed = True
        self._handler.remove_callbacks(self._delayed_show)
        self._posted_show = False
        diff = now_millis() - self._start_time
        if diff >= self._min_show_time or self._start_time == -1:
            self._super_dismiss()
        else:
            if not self._posted_hide:
                self._handler.post_delayed(self._delayed_hide, self._min_show_time - diff)
                self._posted_hide = True

    def show(self):
        self._start_time = -1
        self._dismissed = False
        self._handler.remove_callbacks(self._delayed_hide)
        self._posted_hide = False
        if not self._posted_show:
            self._handler.post_delayed(self._delayed_show, self._min_delay)
            self._posted_show = True
