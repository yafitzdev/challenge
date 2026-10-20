package app.arcopypaste.research.prototypes.text;

import static org.junit.Assert.*;
import org.junit.Test;
import org.mockito.Mockito;
import android.graphics.Bitmap;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestParams;

public class DesktopHTTPClientPublicTest {

    @Test
    public void testGetAbsoluteUrlWithDifferentSuffix() throws Exception {
        // Use reflection since method is private.
        java.lang.reflect.Method method = DesktopHTTPClient.class.getDeclaredMethod("getAbsoluteUrl", String.class);
        method.setAccessible(true);
        String url = (String)method.invoke(null, "/public-data");
        assertTrue(url.endsWith("/public-data") || url.contains("/public-data"));
    }

    @Test
    public void testSetDifferentPositionAndNoCrash() {
        // The method has no return, will call AsyncHttpClient.get. Just test invocation.
        DesktopHTTPClient.setPosition(5.5, -3.3);
    }

    @Test
    public void testSetTextWithDifferentInputAndNoCrash() {
        DesktopHTTPClient.setText("This is a public test string!");
    }

    @Test
    public void testPasteAndNoCrash_Public() {
        // Call again with no return, just coverage
        DesktopHTTPClient.paste();
    }

    @Test
    public void testGetScreenshotReturnsNull_Public() {
        DesktopHTTPClientCallback cb = Mockito.mock(DesktopHTTPClientCallback.class);
        Bitmap result = DesktopHTTPClient.getScreenshot(cb);
        assertNull(result);
    }
}