package com.tasomaniac.android.widget;

import android.app.Application;
import android.app.ProgressDialog;
import android.os.Handler;
import android.os.Looper;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mockito;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;
import org.robolectric.Shadows;
import org.robolectric.annotation.Config;
import org.robolectric.shadows.ShadowLooper;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.spy;
import static org.mockito.Mockito.verify;

@RunWith(RobolectricTestRunner.class)
@Config(sdk = 28) // Target SDK for Robolectric
public class DelayedProgressDialogTest {

    private Application application;
    private Handler mockHandler;
    private ShadowLooper shadowLooper;

    @Before
    public void setUp() {
        application = RuntimeEnvironment.getApplication();
        // Spy on a real Handler to capture runnables, but control its execution via ShadowLooper
        mockHandler = spy(new Handler(Looper.getMainLooper()));
        shadowLooper = Shadows.shadowOf(Looper.getMainLooper());
    }

    // Helper to create a dialog with a spied handler for testing
    private DelayedProgressDialog createDialogWithSpiedHandler(int themeResId) {
        return new DelayedProgressDialog(application, themeResId) {
            // Override the handler creation to inject our mockHandler
            @Override
            protected Handler getHandler() { // Assuming there is a getHandler or inject it, or make Handler non-final in prod code
                return mockHandler;
            }
        };
    }

    // Helper to create a dialog with a spied handler for testing (default constructor)
    private DelayedProgressDialog createDialogWithSpiedHandler() {
        return new DelayedProgressDialog(application) {
            @Override
            protected Handler getHandler() {
                return mockHandler;
            }
        };
    }

    // Test helper to allow injecting mock handler (requires small change in prod code or use reflection)
    // For now, I'll rely on the default handler and control it via ShadowLooper directly,
    // as mocking handler directly for postDelayed is tricky without changing prod code.
    // Let's re-evaluate: DelayedProgressDialog creates its own Handler internally.
    // To properly test the Handler interactions (postDelayed, removeCallbacks),
    // I need to either inject a mock Handler or control the Looper directly using Robolectric.
    // Controlling the Looper is the standard Robolectric way.

    // Let's remove the spied handler creation for now and rely on ShadowLooper.
    // The internal Handler is implicitly managed by Looper.getMainLooper(), which Robolectric shadows.

    @Test
    public void testMakeMethods() {
        assertNotNull(DelayedProgressDialog.make(application, "title", "message"));
        assertNotNull(DelayedProgressDialog.make(application, "title", "message", true));
        assertNotNull(DelayedProgressDialog.make(application, "title", "message", true, true));
        assertNotNull(DelayedProgressDialog.make(application, "title", "message", true, true, null));
        // Test with theme
        DelayedProgressDialog dialogWithTheme = new DelayedProgressDialog(application, android.R.style.Theme_Dialog);
        assertNotNull(dialogWithTheme);
    }

    @Test
    public void testShowDelayedMethods() {
        DelayedProgressDialog.showDelayed(application, "title", "message").dismiss();
        DelayedProgressDialog.showDelayed(application, "title", "message", true).dismiss();
        DelayedProgressDialog.showDelayed(application, "title", "message", true, true).dismiss();
        DelayedProgressDialog.showDelayed(application, "title", "message", true, true, null).dismiss();
        // No asserts on dialog visibility here, just that creation works
    }

    @Test
    public void testDismissBeforeMinDelay_shouldNotShow() {
        DelayedProgressDialog dialog = new DelayedProgressDialog(application);
        dialog.setMinDelay(1000);
        dialog.setMinShowTime(500); // Should be irrelevant if it never shows

        dialog.show(); // Posts mDelayedShow

        assertFalse(dialog.isShowing()); // Not yet shown

        shadowLooper.idleFor(200); // Pass some time, but less than minDelay
        assertFalse(dialog.isShowing());

        dialog.dismiss(); // Calls removeCallbacks on mDelayedShow

        shadowLooper.idleFor(1000); // Pass enough time for mDelayedShow to have run if not removed
        assertFalse(dialog.isShowing()); // Should still not be showing
    }

    @Test
    public void testDismissAfterMinDelayButBeforeMinShowTime_shouldShowForMinShowTime() {
        DelayedProgressDialog dialog = new DelayedProgressDialog(application);
        dialog.setMinDelay(500);
        dialog.setMinShowTime(1000);

        dialog.show(); // Posts mDelayedShow

        assertFalse(dialog.isShowing()); // Not yet shown

        shadowLooper.idleFor(500); // Advance past minDelay
        assertTrue(dialog.isShowing()); // Now it should be showing

        shadowLooper.idleFor(200); // Pass some time while showing, but not minShowTime yet

        dialog.dismiss(); // Should post mDelayedHide for remaining minShowTime

        assertTrue(dialog.isShowing()); // Still showing

        shadowLooper.idleFor(799); // Pass almost enough time for minShowTime
        assertTrue(dialog.isShowing());

        shadowLooper.idleFor(1); // Pass the remaining time
        assertFalse(dialog.isShowing()); // Now it should be dismissed
    }

    @Test
    public void testDismissAfterMinShowTime_shouldDismissImmediately() {
        DelayedProgressDialog dialog = new DelayedProgressDialog(application);
        dialog.setMinDelay(500);
        dialog.setMinShowTime(1000);

        dialog.show(); // Posts mDelayedShow

        assertFalse(dialog.isShowing()); // Not yet shown

        shadowLooper.idleFor(500); // Advance past minDelay
        assertTrue(dialog.isShowing()); // Now it should be showing

        shadowLooper.idleFor(1000); // Advance past minShowTime
        assertTrue(dialog.isShowing()); // Still showing, as dismiss not called yet

        dialog.dismiss(); // Should dismiss immediately

        assertFalse(dialog.isShowing()); // Should be dismissed
    }

    @Test
    public void testShowWithZeroMinDelay_showsImmediately() {
        DelayedProgressDialog dialog = new DelayedProgressDialog(application);
        dialog.setMinDelay(0);
        dialog.setMinShowTime(500);

        dialog.show();
        assertTrue(dialog.isShowing()); // Should be showing immediately

        dialog.dismiss(); // Will trigger minShowTime logic
        shadowLooper.idleFor(500);
        assertFalse(dialog.isShowing());
    }

    @Test
    public void testDismissWhenNeverShown_noOp() {
        DelayedProgressDialog dialog = new DelayedProgressDialog(application);
        dialog.setMinDelay(1000);
        dialog.show(); // Posts show, but not executed yet
        assertFalse(dialog.isShowing());

        dialog.dismiss(); // Dismissed flag set, show callback removed
        assertFalse(dialog.isShowing()); // Still not showing

        shadowLooper.idleFor(2000); // Advance past any potential delays
        assertFalse(dialog.isShowing()); // Still not showing
    }

    @Test
    public void testOnDetachedFromWindowRemovesCallbacks() {
        DelayedProgressDialog dialog = new DelayedProgressDialog(application);
        Handler spyHandler = spy(new Handler(Looper.getMainLooper()));
        // Use reflection or a test-specific method to inject handler if not available
        // For now, let's assume it uses Looper.getMainLooper() internally
        // which Robolectric controls.
        // We can verify removed callbacks by checking ShadowLooper.getSchedulableEvents().

        dialog.show(); // Posts mDelayedShow
        assertTrue(shadowLooper.getScheduledPostCallbacks().size() == 1);

        // Simulate onDetachedFromWindow
        dialog.onDetachedFromWindow();

        assertTrue(shadowLooper.getScheduledPostCallbacks().isEmpty()); // Both should be removed

        dialog.dismiss(); // No-op for handlers, but mDismissed set
        shadowLooper.idleFor(2000); // Advance time
        assertFalse(dialog.isShowing());
    }

    @Test
    public void testSetMinShowTime() {
        DelayedProgressDialog dialog = new DelayedProgressDialog(application);
        dialog.setMinShowTime(2000); // Set to 2 seconds
        dialog.setMinDelay(0); // Show immediately
        dialog.show();
        assertTrue(dialog.isShowing());
        dialog.dismiss(); // Now it will wait 2 seconds
        shadowLooper.idleFor(1999);
        assertTrue(dialog.isShowing());
        shadowLooper.idleFor(1);
        assertFalse(dialog.isShowing());
    }

    @Test
    public void testSetMinDelay() {
        DelayedProgressDialog dialog = new DelayedProgressDialog(application);
        dialog.setMinDelay(2000); // Set to 2 seconds
        dialog.setMinShowTime(0); // Dismiss immediately after showing
        dialog.show();
        assertFalse(dialog.isShowing()); // Not yet shown

        shadowLooper.idleFor(1999);
        assertFalse(dialog.isShowing()); // Still not shown

        shadowLooper.idleFor(1);
        assertTrue(dialog.isShowing()); // Now shown

        dialog.dismiss(); // Should dismiss immediately because minShowTime is 0
        assertFalse(dialog.isShowing());
    }

    @Test
    public void testMultipleShowDismissCycles() {
        DelayedProgressDialog dialog = new DelayedProgressDialog(application);
        dialog.setMinDelay(100);
        dialog.setMinShowTime(200);

        // Cycle 1: Show, then dismiss before min delay
        dialog.show();
        shadowLooper.idleFor(50);
        dialog.dismiss();
        shadowLooper.idleFor(500);
        assertFalse(dialog.isShowing());

        // Cycle 2: Show, let it show, then dismiss after min show time
        dialog.show();
        shadowLooper.idleFor(100); // Pass minDelay
        assertTrue(dialog.isShowing());
        shadowLooper.idleFor(200); // Pass minShowTime
        assertTrue(dialog.isShowing());
        dialog.dismiss();
        assertFalse(dialog.isShowing());

        // Cycle 3: Show, let it show, then dismiss before min show time
        dialog.show();
        shadowLooper.idleFor(100); // Pass minDelay
        assertTrue(dialog.isShowing());
        shadowLooper.idleFor(100); // Before minShowTime is over
        assertTrue(dialog.isShowing());
        dialog.dismiss(); // Should post delayed hide
        assertTrue(dialog.isShowing());
        shadowLooper.idleFor(100); // Remaining minShowTime
        assertFalse(dialog.isShowing());
    }
}