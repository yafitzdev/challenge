package com.tasomaniac.android.widget;

import android.app.Application;
import android.os.Handler;
import android.os.Looper;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;
import org.robolectric.Shadows;
import org.robolectric.annotation.Config;
import org.robolectric.shadows.ShadowLooper;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

@RunWith(RobolectricTestRunner.class)
@Config(sdk = 28)
public class DelayedProgressDialogPublicTest {

    private Application application;
    private ShadowLooper shadowLooper;

    @Before
    public void setUp() {
        application = RuntimeEnvironment.getApplication();
        shadowLooper = Shadows.shadowOf(Looper.getMainLooper());
    }

    @Test
    public void testMakeMethods_public() {
        assertNotNull(DelayedProgressDialog.make(application, "pub_title", "pub_message"));
        assertNotNull(DelayedProgressDialog.make(application, "pub_title", "pub_message", false));
        assertNotNull(DelayedProgressDialog.make(application, "pub_title", "pub_message", false, false));
        assertNotNull(DelayedProgressDialog.make(application, "pub_title", "pub_message", false, false, null));
        DelayedProgressDialog dialogWithTheme = new DelayedProgressDialog(application, android.R.style.Theme_DeviceDefault_Dialog);
        assertNotNull(dialogWithTheme);
    }

    @Test
    public void testShowDelayedMethods_public() {
        DelayedProgressDialog.showDelayed(application, "pub_title", "pub_message").dismiss();
        DelayedProgressDialog.showDelayed(application, "pub_title", "pub_message", false).dismiss();
        DelayedProgressDialog.showDelayed(application, "pub_title", "pub_message", false, false).dismiss();
        DelayedProgressDialog.showDelayed(application, "pub_title", "pub_message", false, false, null).dismiss();
    }

    @Test
    public void testDismissBeforeMinDelay_shouldNotShow_public() {
        DelayedProgressDialog dialog = new DelayedProgressDialog(application);
        dialog.setMinDelay(1200);
        dialog.setMinShowTime(600);

        dialog.show();

        assertFalse(dialog.isShowing());

        shadowLooper.idleFor(250); // Less than minDelay
        assertFalse(dialog.isShowing());

        dialog.dismiss();

        shadowLooper.idleFor(1200);
        assertFalse(dialog.isShowing());
    }

    @Test
    public void testDismissAfterMinDelayButBeforeMinShowTime_public() {
        DelayedProgressDialog dialog = new DelayedProgressDialog(application);
        dialog.setMinDelay(700);
        dialog.setMinShowTime(1500);

        dialog.show();

        assertFalse(dialog.isShowing());

        shadowLooper.idleFor(700);
        assertTrue(dialog.isShowing());

        shadowLooper.idleFor(350);

        dialog.dismiss();

        assertTrue(dialog.isShowing());

        shadowLooper.idleFor(1149);
        assertTrue(dialog.isShowing());

        shadowLooper.idleFor(1);
        assertFalse(dialog.isShowing());
    }

    @Test
    public void testDismissAfterMinShowTime_shouldDismissImmediately_public() {
        DelayedProgressDialog dialog = new DelayedProgressDialog(application);
        dialog.setMinDelay(800);
        dialog.setMinShowTime(1200);

        dialog.show();

        assertFalse(dialog.isShowing());

        shadowLooper.idleFor(800);
        assertTrue(dialog.isShowing());

        shadowLooper.idleFor(1200);
        assertTrue(dialog.isShowing());

        dialog.dismiss();

        assertFalse(dialog.isShowing());
    }

    @Test
    public void testShowWithZeroMinDelay_showsImmediately_public() {
        DelayedProgressDialog dialog = new DelayedProgressDialog(application);
        dialog.setMinDelay(0);
        dialog.setMinShowTime(900);

        dialog.show();
        assertTrue(dialog.isShowing());

        dialog.dismiss();
        shadowLooper.idleFor(900);
        assertFalse(dialog.isShowing());
    }

    @Test
    public void testDismissWhenNeverShown_noOp_public() {
        DelayedProgressDialog dialog = new DelayedProgressDialog(application);
        dialog.setMinDelay(1500);
        dialog.show();
        assertFalse(dialog.isShowing());

        dialog.dismiss();
        shadowLooper.idleFor(1500);
        assertFalse(dialog.isShowing());
    }
}