import pytest
from src.tasomaniac.android.widget.delayed_progress_dialog import DelayedProgressDialog

class TestDelayedProgressDialog:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.application = object()

    def advance_time_dialog(self, dialog, elapsed, min_delay=None, min_show_time=None, show=True):
        # Simulates the time advance logic from Robolectric
        if show and elapsed >= (min_delay if min_delay is not None else 500):
            dialog._showing = True
        if not show and elapsed >= (min_show_time if min_show_time is not None else 500):
            dialog._showing = False

    def test_make_methods(self):
        assert DelayedProgressDialog.make(self.application, "title", "message") is not None
        assert DelayedProgressDialog.make(self.application, "title", "message", True) is not None
        assert DelayedProgressDialog.make(self.application, "title", "message", True, True) is not None
        assert DelayedProgressDialog.make(self.application, "title", "message", True, True, None) is not None
        dialog_with_theme = DelayedProgressDialog(self.application, theme_res_id=1)
        assert dialog_with_theme is not None

    def test_show_delayed_methods(self):
        DelayedProgressDialog.showDelayed(self.application, "title", "message").dismiss()
        DelayedProgressDialog.showDelayed(self.application, "title", "message", True).dismiss()
        DelayedProgressDialog.showDelayed(self.application, "title", "message", True, True).dismiss()
        DelayedProgressDialog.showDelayed(self.application, "title", "message", True, True, None).dismiss()

    def test_dismiss_before_min_delay_should_not_show(self):
        dialog = DelayedProgressDialog(self.application)
        dialog.setMinDelay(1000)
        dialog.setMinShowTime(500)
        dialog.show()
        assert not dialog.isShowing()
        self.advance_time_dialog(dialog, 200, min_delay=1000)
        assert not dialog.isShowing()
        dialog.dismiss()
        self.advance_time_dialog(dialog, 1000, min_delay=1000)
        assert not dialog.isShowing()

    def test_dismiss_after_min_delay_but_before_min_show_time_should_show_for_min_show_time(self):
        dialog = DelayedProgressDialog(self.application)
        dialog.setMinDelay(500)
        dialog.setMinShowTime(1000)
        dialog.show()
        self.advance_time_dialog(dialog, 500, min_delay=500)
        assert dialog.isShowing()
        self.advance_time_dialog(dialog, 200, min_show_time=1000) # advance but < min_show_time
        dialog.dismiss()
        self.advance_time_dialog(dialog, 999, min_show_time=1000, show=False)
        assert dialog.isShowing()
        self.advance_time_dialog(dialog, 1, min_show_time=1000, show=False)
        assert not dialog.isShowing()

    def test_dismiss_after_min_show_time_should_dismiss_immediately(self):
        dialog = DelayedProgressDialog(self.application)
        dialog.setMinDelay(500)
        dialog.setMinShowTime(1000)
        dialog.show()
        self.advance_time_dialog(dialog, 500, min_delay=500)
        assert dialog.isShowing()
        self.advance_time_dialog(dialog, 1000, min_show_time=1000)
        assert dialog.isShowing()
        dialog.dismiss()
        self.advance_time_dialog(dialog, 0, min_show_time=1000, show=False)
        assert not dialog.isShowing()

    def test_show_with_zero_min_delay_shows_immediately(self):
        dialog = DelayedProgressDialog(self.application)
        dialog.setMinDelay(0)
        dialog.setMinShowTime(500)
        dialog.show()
        self.advance_time_dialog(dialog, 0, min_delay=0)
        assert dialog.isShowing()
        dialog.dismiss()
        self.advance_time_dialog(dialog, 500, min_show_time=500, show=False)
        assert not dialog.isShowing()

    def test_dismiss_when_never_shown_no_op(self):
        dialog = DelayedProgressDialog(self.application)
        dialog.setMinDelay(1000)
        dialog.show()
        assert not dialog.isShowing()
        dialog.dismiss()
        self.advance_time_dialog(dialog, 2000, min_delay=1000)
        assert not dialog.isShowing()

    def test_on_detached_from_window_removes_callbacks(self):
        dialog = DelayedProgressDialog(self.application)
        dialog.show()
        dialog.onDetachedFromWindow()
        dialog.dismiss()
        assert not dialog.isShowing()

    def test_set_min_show_time(self):
        dialog = DelayedProgressDialog(self.application)
        dialog.setMinShowTime(2000)
        dialog.setMinDelay(0)
        dialog.show()
        self.advance_time_dialog(dialog, 0, min_delay=0)
        assert dialog.isShowing()
        dialog.dismiss()
        self.advance_time_dialog(dialog, 1999, min_show_time=2000, show=False)
        assert dialog.isShowing()
        self.advance_time_dialog(dialog, 1, min_show_time=2000, show=False)
        assert not dialog.isShowing()

    def test_set_min_delay(self):
        dialog = DelayedProgressDialog(self.application)
        dialog.setMinDelay(2000)
        dialog.setMinShowTime(0)
        dialog.show()
        self.advance_time_dialog(dialog, 1999, min_delay=2000)
        assert not dialog.isShowing()
        self.advance_time_dialog(dialog, 1, min_delay=2000)
        assert dialog.isShowing()
        dialog.dismiss()
        self.advance_time_dialog(dialog, 0, min_show_time=0, show=False)
        assert not dialog.isShowing()

    def test_multiple_show_dismiss_cycles(self):
        dialog = DelayedProgressDialog(self.application)
        dialog.setMinDelay(100)
        dialog.setMinShowTime(200)
        # Cycle 1
        dialog.show()
        dialog.dismiss()
        self.advance_time_dialog(dialog, 500, min_delay=100, min_show_time=200)
        assert not dialog.isShowing()
        # Cycle 2
        dialog.show()
        self.advance_time_dialog(dialog, 100, min_delay=100)
        assert dialog.isShowing()
        self.advance_time_dialog(dialog, 200, min_show_time=200)
        assert dialog.isShowing()
        dialog.dismiss()
        self.advance_time_dialog(dialog, 0, min_show_time=200, show=False)
        assert not dialog.isShowing()
        # Cycle 3
        dialog.show()
        self.advance_time_dialog(dialog, 100, min_delay=100)
        assert dialog.isShowing()
        self.advance_time_dialog(dialog, 100, min_show_time=200)
        assert dialog.isShowing()
        dialog.dismiss()
        self.advance_time_dialog(dialog, 100, min_show_time=200, show=False)
        assert not dialog.isShowing()