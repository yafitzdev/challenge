package app.arcopypaste.research.prototypes.text;

import static org.junit.Assert.*;
import org.junit.Test;
import org.mockito.Mockito;
import android.graphics.Bitmap;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestParams;

public class DesktopHTTPClientTest {

    @Test
    public void testGetAbsoluteUrl() throws Exception {
        // Use reflection since method is private.
        java.lang.reflect.Method method = DesktopHTTPClient.class.getDeclaredMethod("getAbsoluteUrl", String.class);
        method.setAccessible(true);
        String url = (String)method.invoke(null, "/test");
        assertTrue(url.contains("/test"));
    }

    @Test
    public void testSetPositionAndNoCrash() {
        // The method has no return, will call AsyncHttpClient.get. Just test invocation.
        DesktopHTTPClient.setPosition(1.0, 2.0);
    }

    @Test
    public void testSetTextAndNoCrash() {
        DesktopHTTPClient.setText("Hello World");
    }

    @Test
    public void testPasteAndNoCrash() {
        DesktopHTTPClient.paste();
    }

    @Test
    public void testGetScreenshotReturnsNull() {
        DesktopHTTPClientCallback cb = Mockito.mock(DesktopHTTPClientCallback.class);
        Bitmap result = DesktopHTTPClient.getScreenshot(cb);
        assertNull(result);
    }
}