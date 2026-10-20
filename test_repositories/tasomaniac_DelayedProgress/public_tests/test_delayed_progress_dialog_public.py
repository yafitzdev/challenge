import pytest
from src.tasomaniac.android.widget.delayed_progress_dialog import DelayedProgressDialog

class TestDelayedProgressDialogPublic:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.application = object()

    def advance_time_dialog(self, dialog, elapsed, min_delay=None, min_show_time=None, show=True):
        if show and elapsed >= (min_delay if min_delay is not None else dialog._min_delay):
            dialog._showing = True
        if not show and elapsed >= (min_show_time if min_show_time is not None else dialog._min_show_time):
            dialog._showing = False

    def test_make_methods_public(self):
        assert DelayedProgressDialog.make(self.application, "pub_title", "pub_message") is not None
        assert DelayedProgressDialog.make(self.application, "pub_title", "pub_message", False) is not None
        assert DelayedProgressDialog.make(self.application, "pub_title", "pub_message", False, False) is not None
        assert DelayedProgressDialog.make(self.application, "pub_title", "pub_message", False, False, None) is not None
        dialog_with_theme = DelayedProgressDialog(self.application, theme_res_id=1)
        assert dialog_with_theme is not None

    def test_show_delayed_methods_public(self):
        DelayedProgressDialog.showDelayed(self.application, "pub_title", "pub_message").dismiss()
        DelayedProgressDialog.showDelayed(self.application, "pub_title", "pub_message", False).dismiss()
        DelayedProgressDialog.showDelayed(self.application, "pub_title", "pub_message", False, False).dismiss()
        DelayedProgressDialog.showDelayed(self.application, "pub_title", "pub_message", False, False, None).dismiss()

    def test_dismiss_before_min_delay_should_not_show_public(self):
        dialog = DelayedProgressDialog(self.application)
        dialog.setMinDelay(1200)
        dialog.setMinShowTime(600)
        dialog.show()
        assert not dialog.isShowing()
        self.advance_time_dialog(dialog, 250, min_delay=1200)
        assert not dialog.isShowing()
        dialog.dismiss()
        self.advance_time_dialog(dialog, 1200, min_delay=1200)
        assert not dialog.isShowing()

    def test_dismiss_after_min_delay_but_before_min_show_time_public(self):
        dialog = DelayedProgressDialog(self.application)
        dialog.setMinDelay(700)
        dialog.setMinShowTime(1500)
        dialog.show()
        self.advance_time_dialog(dialog, 700, min_delay=700)
        assert dialog.isShowing()
        self.advance_time_dialog(dialog, 350)
        dialog.dismiss()
        self.advance_time_dialog(dialog, 1149, min_show_time=1500, show=False)
        assert dialog.isShowing()
        self.advance_time_dialog(dialog, 1, min_show_time=1500, show=False)
        assert not dialog.isShowing()

    def test_dismiss_after_min_show_time_should_dismiss_immediately_public(self):
        dialog = DelayedProgressDialog(self.application)
        dialog.setMinDelay(800)
        dialog.setMinShowTime(1200)
        dialog.show()
        self.advance_time_dialog(dialog, 800, min_delay=800)
        assert dialog.isShowing()
        self.advance_time_dialog(dialog, 1200, min_show_time=1200)
        assert dialog.isShowing()
        dialog.dismiss()
        self.advance_time_dialog(dialog, 0, min_show_time=1200, show=False)
        assert not dialog.isShowing()

    def test_show_with_zero_min_delay_shows_immediately_public(self):
        dialog = DelayedProgressDialog(self.application)
        dialog.setMinDelay(0)
        dialog.setMinShowTime(900)
        dialog.show()
        self.advance_time_dialog(dialog, 0, min_delay=0)
        assert dialog.isShowing()
        dialog.dismiss()
        self.advance_time_dialog(dialog, 900, min_show_time=900, show=False)
        assert not dialog.isShowing()

    def test_dismiss_when_never_shown_no_op_public(self):
        dialog = DelayedProgressDialog(self.application)
        dialog.setMinDelay(1500)
        dialog.show()
        assert not dialog.isShowing()
        dialog.dismiss()
        self.advance_time_dialog(dialog, 1500, min_delay=1500)
        assert not dialog.isShowing()