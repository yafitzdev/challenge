package com.tasomaniac.android.widget;

import android.app.Application;
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
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

@RunWith(RobolectricTestRunner.class)
@Config(sdk = 28)
public class DelayedProgressBarPublicTest {

    private Application application;
    private ShadowLooper shadowLooper;

    @Before
    public void setUp() {
        application = RuntimeEnvironment.getApplication();
        shadowLooper = Shadows.shadowOf(Looper.getMainLooper());
    }

    @Test
    public void testConstructors_public() {
        DelayedProgressBar progressBar1 = new DelayedProgressBar(application);
        assertFalse(progressBar1.isShown());
        DelayedProgressBar progressBar2 = new DelayedProgressBar(application, null);
        assertFalse(progressBar2.isShown());
    }

    @Test
    public void testShow_noDelay_public() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        progressBar.setMinDelay(300); // Different from default in original tests
        progressBar.setMinShowTime(700);
        progressBar.show();
        assertEquals(View.GONE, progressBar.getVisibility());
        shadowLooper.idleFor(300); // Advance to our new MinDelay
        assertEquals(View.VISIBLE, progressBar.getVisibility());
        assertEquals(0f, progressBar.getAlpha(), 0.001f);
    }

    @Test
    public void testShow_withAnimation_public() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        progressBar.setAlpha(0f);
        progressBar.setMinDelay(350);
        progressBar.show(true);
        assertEquals(View.GONE, progressBar.getVisibility());
        shadowLooper.idleFor(350);
        assertEquals(View.VISIBLE, progressBar.getVisibility());
        assertEquals(1.0f, progressBar.getAlpha(), 0.001f);
    }

    @Test
    public void testShow_withAnimationAndEndAction_public() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        Runnable endAction = mock(Runnable.class);
        progressBar.setAlpha(0f);
        progressBar.setMinDelay(250);
        progressBar.show(true, endAction);
        shadowLooper.idleFor(250);
        assertEquals(View.VISIBLE, progressBar.getVisibility());
        verify(endAction, times(1)).run();
    }

    @Test
    public void testHideBeforeMinDelay_shouldNotShow_public() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        progressBar.setMinDelay(400);
        progressBar.show();
        assertEquals(View.GONE, progressBar.getVisibility());
        shadowLooper.idleFor(150); // Less than MinDelay
        assertEquals(View.GONE, progressBar.getVisibility());
        progressBar.hide();
        shadowLooper.idleFor(400);
        assertEquals(View.GONE, progressBar.getVisibility());
    }

    @Test
    public void testHideAfterMinDelayButBeforeMinShowTime_public() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        progressBar.setMinDelay(350);
        progressBar.setMinShowTime(650);
        progressBar.show();
        shadowLooper.idleFor(350);
        assertEquals(View.VISIBLE, progressBar.getVisibility());
        shadowLooper.idleFor(250);
        assertEquals(View.VISIBLE, progressBar.getVisibility());
        progressBar.hide();
        assertEquals(View.VISIBLE, progressBar.getVisibility());
        shadowLooper.idleFor(399);
        assertEquals(View.VISIBLE, progressBar.getVisibility());
        shadowLooper.idleFor(1);
        assertEquals(View.GONE, progressBar.getVisibility());
    }

    @Test
    public void testHideAfterMinShowTime_shouldHideImmediately_public() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        progressBar.setMinDelay(280);
        progressBar.setMinShowTime(420);
        progressBar.show();
        shadowLooper.idleFor(280);
        assertEquals(View.VISIBLE, progressBar.getVisibility());
        shadowLooper.idleFor(420);
        assertEquals(View.VISIBLE, progressBar.getVisibility());
        progressBar.hide();
        assertEquals(View.GONE, progressBar.getVisibility());
    }

    @Test
    public void testHideWithAnimation_hidesWithFade_public() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        progressBar.setMinDelay(220);
        progressBar.setMinShowTime(330);
        progressBar.show();
        shadowLooper.idleFor(220);
        progressBar.setAlpha(1.0f);
        progressBar.hide(true);
        assertEquals(View.VISIBLE, progressBar.getVisibility());
        shadowLooper.idleFor(330);
        assertEquals(View.GONE, progressBar.getVisibility());
        assertEquals(0f, progressBar.getAlpha(), 0.001f);
    }

    @Test
    public void testHideWithAnimationAndEndAction_hidesWithFadeAndRunsEndAction_public() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        Runnable endAction = mock(Runnable.class);
        progressBar.setMinDelay(420);
        progressBar.setMinShowTime(350);
        progressBar.show();
        shadowLooper.idleFor(420);
        progressBar.setAlpha(1.0f);
        progressBar.hide(true, endAction);
        assertEquals(View.VISIBLE, progressBar.getVisibility());
        shadowLooper.idleFor(350);
        assertEquals(View.GONE, progressBar.getVisibility());
        verify(endAction, times(1)).run();
    }

    @Test
    public void testOnDetachedFromWindowRemovesCallbacks_public() {
        DelayedProgressBar progressBar = new DelayedProgressBar(application);
        progressBar.setMinDelay(290);
        progressBar.show();
        assertTrue(shadowLooper.getScheduledPostCallbacks().size() == 1);

        progressBar.onDetachedFromWindow();
        assertTrue(shadowLooper.getScheduledPostCallbacks().isEmpty());

        progressBar.setMinDelay(310);
        progressBar.show();
        shadowLooper.idleFor(310);
        progressBar.hide();
        assertTrue(shadowLooper.getScheduledPostCallbacks().size() == 1);

        progressBar.onDetachedFromWindow();
        assertTrue(shadowLooper.getScheduledPostCallbacks().isEmpty());
    }
}