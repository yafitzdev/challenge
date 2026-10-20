package com.tasomaniac.android.widget;

import android.app.Application;
import android.os.Handler;
import android.os.Looper;
import android.view.View;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;
import org.robolectric.Shadows;
import org.robolectric.annotation.Config;
import org.robolectric.shadows.ShadowLooper;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

@RunWith(RobolectricTestRunner.class)
@Config(sdk = 28) // Target SDK for Robolectric
public class DelayedProgressBarTest {

    private Application application;
    private ShadowLooper shadowLooper;

    @Before
    public void setUp() {
        application = RuntimeEnvironment.getApplication();
        shadowLooper = Shadows.shadowOf(Looper.getMainLooper());
    }

    @Test
    public void testConstructors() {
        DelayedProgressBar progressBar1 = new DelayedProgressBar(application);
        assertFalse(progressBar1.isShown());
        DelayedProgressBar progressBar2 = new DelayedProgressBar(application, null);
        assertFalse(progressBar2.isShown());
    }

    @Test
    public void testShow_noDelay() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        progressBar.show();
        // Default MIN_DELAY is 500ms. Without advancing time, it should not be visible immediately.
        assertEquals(View.GONE, progressBar.getVisibility());
        shadowLooper.idleFor(500); // Advance past MIN_DELAY
        assertEquals(View.VISIBLE, progressBar.getVisibility());
        // Default MIN_SHOW_TIME is 500ms
        assertEquals(0f, progressBar.getAlpha(), 0.001f); // No animation means alpha is 1 by default, but ViewCompat animation sets it to 0f initially then to 1f.
    }

    @Test
    public void testShow_withAnimation() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        progressBar.setAlpha(0f); // Pre-set alpha to 0 for animation test
        assertEquals(0f, progressBar.getAlpha(), 0.001f);
        progressBar.show(true); // show with animation
        assertEquals(View.GONE, progressBar.getVisibility());
        shadowLooper.idleFor(500); // Advance past MIN_DELAY
        assertEquals(View.VISIBLE, progressBar.getVisibility());
        assertEquals(1.0f, progressBar.getAlpha(), 0.001f); // Should be faded in to 1.0f
    }

    @Test
    public void testShow_withAnimationAndEndAction() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        Runnable endAction = mock(Runnable.class);
        progressBar.setAlpha(0f);
        progressBar.show(true, endAction);
        shadowLooper.idleFor(500);
        assertEquals(View.VISIBLE, progressBar.getVisibility());
        verify(endAction, times(1)).run(); // End action should run after animation completes (after idleFor)
    }

    @Test
    public void testHideBeforeMinDelay_shouldNotShow() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        progressBar.show(); // Posts mDelayedShow
        assertEquals(View.GONE, progressBar.getVisibility()); // Not yet visible

        shadowLooper.idleFor(200); // Advance less than MIN_DELAY
        assertEquals(View.GONE, progressBar.getVisibility());

        progressBar.hide(); // Cancels mDelayedShow
        shadowLooper.idleFor(500); // Advance past MIN_DELAY
        assertEquals(View.GONE, progressBar.getVisibility()); // Should still be GONE
    }

    @Test
    public void testHideAfterMinDelayButBeforeMinShowTime_shouldShowForMinShowTime() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        progressBar.show(); // Posts mDelayedShow

        shadowLooper.idleFor(500); // Advance past MIN_DELAY
        assertEquals(View.VISIBLE, progressBar.getVisibility()); // Now visible

        shadowLooper.idleFor(200); // Advance, but less than MIN_SHOW_TIME (default 500ms)
        assertEquals(View.VISIBLE, progressBar.getVisibility());

        progressBar.hide(); // Posts mDelayedHide for remaining MIN_SHOW_TIME
        assertEquals(View.VISIBLE, progressBar.getVisibility()); // Still visible

        shadowLooper.idleFor(299); // Pass almost enough time
        assertEquals(View.VISIBLE, progressBar.getVisibility());

        shadowLooper.idleFor(1); // Pass remaining time
        assertEquals(View.GONE, progressBar.getVisibility()); // Now hidden
    }

    @Test
    public void testHideAfterMinShowTime_shouldHideImmediately() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        progressBar.show(); // Posts mDelayedShow

        shadowLooper.idleFor(500); // Advance past MIN_DELAY
        assertEquals(View.VISIBLE, progressBar.getVisibility()); // Now visible

        shadowLooper.idleFor(500); // Advance past MIN_SHOW_TIME
        assertEquals(View.VISIBLE, progressBar.getVisibility());

        progressBar.hide(); // Should hide immediately
        assertEquals(View.GONE, progressBar.getVisibility());
    }

    @Test
    public void testHideWithAnimation_hidesWithFade() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        progressBar.show();
        shadowLooper.idleFor(500); // Pass minDelay
        progressBar.setAlpha(1.0f); // Assume it's fully visible
        progressBar.hide(true); // hide with animation
        assertEquals(View.VISIBLE, progressBar.getVisibility()); // Still visible during animation
        shadowLooper.idleFor(500); // Pass minShowTime (if applicable) and fade out time
        assertEquals(View.GONE, progressBar.getVisibility());
        assertEquals(0f, progressBar.getAlpha(), 0.001f);
    }

    @Test
    public void testHideWithAnimationAndEndAction_hidesWithFadeAndRunsEndAction() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        Runnable endAction = mock(Runnable.class);
        progressBar.show();
        shadowLooper.idleFor(500); // Pass minDelay
        progressBar.setAlpha(1.0f);
        progressBar.hide(true, endAction);
        assertEquals(View.VISIBLE, progressBar.getVisibility());
        shadowLooper.idleFor(500); // Pass minShowTime (if applicable) and fade out time
        assertEquals(View.GONE, progressBar.getVisibility());
        verify(endAction, times(1)).run();
    }

    @Test
    public void testOnDetachedFromWindowRemovesCallbacks() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        progressBar.show(); // Posts mDelayedShow
        assertTrue(shadowLooper.getScheduledPostCallbacks().size() == 1);

        progressBar.onDetachedFromWindow(); // Should remove mDelayedShow
        assertTrue(shadowLooper.getScheduledPostCallbacks().isEmpty());

        // Now test if hide callback is also removed
        progressBar.show();
        shadowLooper.idleFor(500); // Show it
        progressBar.hide(); // Posts mDelayedHide
        assertTrue(shadowLooper.getScheduledPostCallbacks().size() == 1);

        progressBar.onDetachedFromWindow(); // Should remove mDelayedHide
        assertTrue(shadowLooper.getScheduledPostCallbacks().isEmpty());
    }

    @Test
    public void testImmediateHideWhenNeverShown() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        progressBar.hide(); // Should directly call doHide as mStartTime is -1
        assertEquals(View.GONE, progressBar.getVisibility()); // Should be GONE immediately
    }

    @Test
    public void testShowAndHideCalledMultipleTimes() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        progressBar.show(); // post mDelayedShow
        shadowLooper.idleFor(100);
        progressBar.hide(); // removes mDelayedShow, calls doHide
        assertEquals(View.GONE, progressBar.getVisibility());

        // Re-show
        progressBar.show(); // post mDelayedShow
        shadowLooper.idleFor(600); // pass minDelay & minShowTime for this instance
        assertEquals(View.VISIBLE, progressBar.getVisibility());
        progressBar.hide(); // should hide immediately
        assertEquals(View.GONE, progressBar.getVisibility());
    }
}