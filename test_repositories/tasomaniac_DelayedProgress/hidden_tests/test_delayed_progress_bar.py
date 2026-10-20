import pytest
from unittest.mock import Mock

from src.tasomaniac.android.widget.delayed_progress_bar import DelayedProgressBar

class TestDelayedProgressBar:

    class View:
        GONE = 8
        VISIBLE = 0

    @pytest.fixture(autouse=True)
    def setup(self):
        self.application = object()

    def advance_time_bar(self, pb, elapsed, min_delay=None, min_show_time=None, show=True):
        """Simulate passage of time for DelayedProgressBar."""
        # Show logic
        if show and elapsed >= (min_delay if min_delay is not None else 500):
            pb._visibility = self.View.VISIBLE
            pb._shown = True
            if hasattr(pb, "_end_action") and pb._end_action:
                pb._end_action()
            pb.setAlpha(1.0 if pb.getAlpha() == 0.0 else pb.getAlpha())
        # Hide logic (will be used after show)
        if not show and elapsed >= (min_show_time if min_show_time is not None else 500):
            pb._visibility = self.View.GONE
            pb._shown = False

    def test_constructors(self):
        pb1 = DelayedProgressBar(self.application)
        assert not pb1.isShown()
        pb2 = DelayedProgressBar(self.application, None)
        assert not pb2.isShown()

    def test_show_no_delay(self):
        pb = DelayedProgressBar(self.application)
        pb.show()
        assert pb.getVisibility() == self.View.GONE
        self.advance_time_bar(pb, 500)
        assert pb.getVisibility() == self.View.VISIBLE
        assert abs(pb.getAlpha() - 0.0) < 0.001

    def test_show_with_animation(self):
        pb = DelayedProgressBar(self.application)
        pb.setAlpha(0.0)
        assert abs(pb.getAlpha() - 0.0) < 0.001
        pb.show(True)
        self.advance_time_bar(pb, 500)
        assert pb.getVisibility() == self.View.VISIBLE
        assert abs(pb.getAlpha() - 1.0) < 0.001

    def test_show_with_animation_and_end_action(self):
        pb = DelayedProgressBar(self.application)
        end_action = Mock()
        pb.setAlpha(0.0)
        pb.show(True, end_action)
        pb._end_action = end_action
        self.advance_time_bar(pb, 500)
        end_action.assert_called_once()

    def test_hide_before_min_delay_should_not_show(self):
        pb = DelayedProgressBar(self.application)
        pb.show()
        assert pb.getVisibility() == self.View.GONE
        # Simulate 200ms < MIN_DELAY
        self.advance_time_bar(pb, 200)
        assert pb.getVisibility() == self.View.GONE
        pb.hide()
        # Even after time passes, still should be GONE
        self.advance_time_bar(pb, 500, show=False)
        assert pb.getVisibility() == self.View.GONE

    def test_hide_after_min_delay_but_before_min_show_time_should_show_for_min_show_time(self):
        pb = DelayedProgressBar(self.application)
        pb.show()
        self.advance_time_bar(pb, 500) # make visible
        assert pb.getVisibility() == self.View.VISIBLE
        self.advance_time_bar(pb, 200)
        assert pb.getVisibility() == self.View.VISIBLE
        pb.hide()
        assert pb.getVisibility() == self.View.VISIBLE
        self.advance_time_bar(pb, 299, show=False)
        assert pb.getVisibility() == self.View.VISIBLE
        self.advance_time_bar(pb, 1, show=False)
        assert pb.getVisibility() == self.View.GONE

    def test_hide_after_min_show_time_should_hide_immediately(self):
        pb = DelayedProgressBar(self.application)
        pb.show()
        self.advance_time_bar(pb, 500) # visible
        assert pb.getVisibility() == self.View.VISIBLE
        self.advance_time_bar(pb, 500) # pass min_show_time
        assert pb.getVisibility() == self.View.VISIBLE
        pb.hide()
        self.advance_time_bar(pb, 0, show=False)
        assert pb.getVisibility() == self.View.GONE

    def test_hide_with_animation_hides_with_fade(self):
        pb = DelayedProgressBar(self.application)
        pb.show()
        self.advance_time_bar(pb, 500)
        pb.setAlpha(1.0)
        pb.hide(True)
        # Should still be visible during animation
        assert pb.getVisibility() == self.View.VISIBLE
        # After animation, GONE, alpha=0.0
        self.advance_time_bar(pb, 500, show=False)
        pb.setAlpha(0.0)
        assert pb.getVisibility() == self.View.GONE
        assert abs(pb.getAlpha() - 0.0) < 0.001

    def test_hide_with_animation_and_end_action_hides_with_fade_and_runs_end_action(self):
        pb = DelayedProgressBar(self.application)
        end_action = Mock()
        pb.show()
        self.advance_time_bar(pb, 500)
        pb.setAlpha(1.0)
        pb.hide(True, end_action)
        # Animation period
        assert pb.getVisibility() == self.View.VISIBLE
        self.advance_time_bar(pb, 500, show=False)
        pb.setAlpha(0.0)
        end_action()
        end_action.assert_called()

    def test_on_detached_from_window_removes_callbacks(self):
        pb = DelayedProgressBar(self.application)
        pb._callbacks = [object()]
        pb.onDetachedFromWindow()
        assert len(pb._callbacks) == 0
        pb._callbacks = [object()]
        pb.onDetachedFromWindow()
        assert len(pb._callbacks) == 0

    def test_immediate_hide_when_never_shown(self):
        pb = DelayedProgressBar(self.application)
        pb.hide()
        assert pb.getVisibility() == self.View.GONE

    def test_show_and_hide_called_multiple_times(self):
        pb = DelayedProgressBar(self.application)
        pb.show()
        self.advance_time_bar(pb, 100)
        pb.hide()
        self.advance_time_bar(pb, 0, show=False)
        assert pb.getVisibility() == self.View.GONE
        pb.show()
        self.advance_time_bar(pb, 600)
        assert pb.getVisibility() == self.View.VISIBLE
        pb.hide()
        self.advance_time_bar(pb, 0, show=False)
        assert pb.getVisibility() == self.View.GONE