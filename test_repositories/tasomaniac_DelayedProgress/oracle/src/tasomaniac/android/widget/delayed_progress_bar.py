"""Python port of com.tasomaniac.android.widget.DelayedProgressBar.

A progress bar that waits a minimum delay before showing, and once shown stays
visible for at least a minimum show time.
"""
from ._handler import now_millis


class View:
    VISIBLE = 0
    INVISIBLE = 4
    GONE = 8


def _empty_end_action():
    pass


class DelayedProgressBar:
    MIN_SHOW_TIME = 500  # ms
    MIN_DELAY = 500  # ms

    def __init__(self, context, attrs=None):
        self._context = context
        self._attrs = attrs
        self._visibility = View.GONE
        self._alpha = 1.0
        self._min_show_time = DelayedProgressBar.MIN_SHOW_TIME
        self._min_delay = DelayedProgressBar.MIN_DELAY
        self._start_time = -1
        self._posted_hide = False
        self._posted_show = False
        self._dismissed = False
        self._animate = False
        self._show_end_action = None
        self._hide_end_action = None
        # pending callbacks posted to this view
        self._callbacks = []

    # ---- "shown" state: mirrors mStartTime being set by the delayed show ----
    @property
    def _shown(self):
        return self._start_time != -1

    @_shown.setter
    def _shown(self, value):
        if value:
            if not self._dismissed:
                self._start_time = now_millis()
        else:
            self._start_time = -1

    # ---- View-like API ----
    def getVisibility(self):
        return self._visibility

    def setVisibility(self, visibility):
        self._visibility = visibility

    def getAlpha(self):
        return self._alpha

    def setAlpha(self, alpha):
        self._alpha = float(alpha)

    def isShown(self):
        return self._visibility == View.VISIBLE

    def setMinShowTime(self, min_show_time):
        self._min_show_time = min_show_time

    def setMinDelay(self, min_delay):
        self._min_delay = min_delay

    def postDelayed(self, runnable, delay):
        self._callbacks.append((runnable, delay))
        return True

    def removeCallbacks(self, runnable=None):
        if runnable is None:
            self._remove_callbacks()
            return
        self._callbacks = [e for e in self._callbacks
                           if not (isinstance(e, tuple) and e[0] == runnable)]

    def runPendingCallbacks(self):
        """Run every pending posted callback (acts as advancing the looper)."""
        pending = self._callbacks
        self._callbacks = []
        for entry in pending:
            if isinstance(entry, tuple):
                entry[0]()

    # ---- runnables ----
    def _delayed_hide(self):
        self._posted_hide = False
        self._do_hide(self._animate)
        self._start_time = -1

    def _delayed_show(self):
        self._posted_show = False
        if not self._dismissed:
            self._start_time = now_millis()
            if self._animate:
                self.setAlpha(0.0)
                self.setVisibility(View.VISIBLE)
                # animation to alpha 1.0 completes immediately
                self.setAlpha(1.0)
                if self._show_end_action is not None:
                    self._show_end_action()
            else:
                self.setVisibility(View.VISIBLE)

    def onDetachedFromWindow(self):
        # detaching the view drops its pending posted callbacks
        self._callbacks = []
        self._remove_callbacks()

    def _remove_callbacks(self):
        self.removeCallbacks(self._delayed_hide)
        self._posted_hide = False
        self.removeCallbacks(self._delayed_show)
        self._posted_show = False

    def hide(self, animate=False, end_action=None):
        if end_action is None:
            end_action = _empty_end_action
        self._animate = animate
        self._hide_end_action = end_action

        self._dismissed = True
        self.removeCallbacks(self._delayed_show)
        self._posted_show = False
        diff = now_millis() - self._start_time
        if diff >= self._min_show_time or self._start_time == -1:
            self._do_hide(animate)
        else:
            if not self._posted_hide:
                self.postDelayed(self._delayed_hide, self._min_show_time - diff)
                self._posted_hide = True

    def _do_hide(self, animate):
        if animate and self._start_time != -1:
            # fade-out animation to alpha 0, completes immediately
            self.setAlpha(0.0)
            self.setVisibility(View.GONE)
            self._hide_end_action()
        else:
            self.setVisibility(View.GONE)
            self._hide_end_action()

    def show(self, animate=False, end_action=None):
        if end_action is None:
            end_action = _empty_end_action
        self._animate = animate
        self._show_end_action = end_action
        self._start_time = -1
        self._dismissed = False
        self.removeCallbacks(self._delayed_hide)
        self._posted_hide = False
        if not self._posted_show:
            self.postDelayed(self._delayed_show, self._min_delay)
            self._posted_show = True
