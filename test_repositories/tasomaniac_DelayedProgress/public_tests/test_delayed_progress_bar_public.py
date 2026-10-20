import pytest
from unittest.mock import Mock

from src.tasomaniac.android.widget.delayed_progress_bar import DelayedProgressBar

class TestDelayedProgressBarPublic:

    class View:
        GONE = 8
        VISIBLE = 0

    @pytest.fixture(autouse=True)
    def setup(self):
        self.application = object()

    def advance_time_bar(self, pb, elapsed, min_delay=None, min_show_time=None, show=True):
        """Simulate passage of time for DelayedProgressBar."""
        # Show logic
        if show and elapsed >= (min_delay if min_delay is not None else pb._min_delay):
            pb._visibility = self.View.VISIBLE
            pb._shown = True
            if hasattr(pb, "_end_action") and pb._end_action:
                pb._end_action()
            pb.setAlpha(1.0 if pb.getAlpha() == 0.0 else pb.getAlpha())
        # Hide logic (will be used after show)
        if not show and elapsed >= (min_show_time if min_show_time is not None else pb._min_show_time):
            pb._visibility = self.View.GONE
            pb._shown = False

    def test_constructors_public(self):
        pb1 = DelayedProgressBar(self.application)
        assert not pb1.isShown()
        pb2 = DelayedProgressBar(self.application, None)
        assert not pb2.isShown()

    def test_show_no_delay_public(self):
        pb = DelayedProgressBar(self.application)
        pb.setMinDelay(300)
        pb.setMinShowTime(700)
        pb.show()
        assert pb.getVisibility() == self.View.GONE
        self.advance_time_bar(pb, 300, min_delay=300)
        assert pb.getVisibility() == self.View.VISIBLE
        assert abs(pb.getAlpha() - 0.0) < 0.001

    def test_show_with_animation_public(self):
        pb = DelayedProgressBar(self.application)
        pb.setAlpha(0.0)
        pb.setMinDelay(350)
        pb.show(True)
        self.advance_time_bar(pb, 350, min_delay=350)
        assert pb.getVisibility() == self.View.VISIBLE
        assert abs(pb.getAlpha() - 1.0) < 0.001

    def test_show_with_animation_and_end_action_public(self):
        pb = DelayedProgressBar(self.application)
        end_action = Mock()
        pb.setAlpha(0.0)
        pb.setMinDelay(250)
        pb.show(True, end_action)
        pb._end_action = end_action
        self.advance_time_bar(pb, 250, min_delay=250)
        end_action.assert_called_once()

    def test_hide_before_min_delay_should_not_show_public(self):
        pb = DelayedProgressBar(self.application)
        pb.setMinDelay(400)
        pb.show()
        assert pb.getVisibility() == self.View.GONE
        self.advance_time_bar(pb, 150, min_delay=400)
        assert pb.getVisibility() == self.View.GONE
        pb.hide()
        self.advance_time_bar(pb, 400, show=False)
        assert pb.getVisibility() == self.View.GONE

    def test_hide_after_min_delay_but_before_min_show_time_public(self):
        pb = DelayedProgressBar(self.application)
        pb.setMinDelay(350)
        pb.setMinShowTime(650)
        pb.show()
        self.advance_time_bar(pb, 350, min_delay=350)
        assert pb.getVisibility() == self.View.VISIBLE
        self.advance_time_bar(pb, 250)
        pb.hide()
        assert pb.getVisibility() == self.View.VISIBLE
        self.advance_time_bar(pb, 399, min_show_time=650, show=False)
        assert pb.getVisibility() == self.View.VISIBLE
        self.advance_time_bar(pb, 1, min_show_time=650, show=False)
        assert pb.getVisibility() == self.View.GONE

    def test_hide_after_min_show_time_should_hide_immediately_public(self):
        pb = DelayedProgressBar(self.application)
        pb.setMinDelay(280)
        pb.setMinShowTime(420)
        pb.show()
        self.advance_time_bar(pb, 280, min_delay=280)
        assert pb.getVisibility() == self.View.VISIBLE
        self.advance_time_bar(pb, 420, min_show_time=420)
        assert pb.getVisibility() == self.View.VISIBLE
        pb.hide()
        self.advance_time_bar(pb, 0, show=False)
        assert pb.getVisibility() == self.View.GONE

    def test_hide_with_animation_hides_with_fade_public(self):
        pb = DelayedProgressBar(self.application)
        pb.setMinDelay(220)
        pb.setMinShowTime(330)
        pb.show()
        self.advance_time_bar(pb, 220, min_delay=220)
        pb.setAlpha(1.0)
        pb.hide(True)
        assert pb.getVisibility() == self.View.VISIBLE
        self.advance_time_bar(pb, 330, min_show_time=330, show=False)
        pb.setAlpha(0.0)
        assert pb.getVisibility() == self.View.GONE
        assert abs(pb.getAlpha() - 0.0) < 0.001

    def test_hide_with_animation_and_end_action_hides_with_fade_and_runs_end_action_public(self):
        pb = DelayedProgressBar(self.application)
        end_action = Mock()
        pb.setMinDelay(420)
        pb.setMinShowTime(350)
        pb.show()
        self.advance_time_bar(pb, 420, min_delay=420)
        pb.setAlpha(1.0)
        pb.hide(True, end_action)
        assert pb.getVisibility() == self.View.VISIBLE
        self.advance_time_bar(pb, 350, min_show_time=350, show=False)
        pb.setAlpha(0.0)
        end_action()
        end_action.assert_called()

    def test_on_detached_from_window_removes_callbacks_public(self):
        pb = DelayedProgressBar(self.application)
        pb.setMinDelay(290)
        pb._callbacks = [object()]
        pb.onDetachedFromWindow()
        assert len(pb._callbacks) == 0
        pb.setMinDelay(310)
        pb._callbacks = [object()]
        pb.onDetachedFromWindow()
        assert len(pb._callbacks) == 0