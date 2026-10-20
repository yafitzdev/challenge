package app.arcopypaste.research.prototypes.text;

import static org.junit.Assert.*;

import org.junit.Test;
import org.junit.Before;
import org.mockito.Mockito;
import android.graphics.Bitmap;

public class TextRecognitionTest {

    @Test
    public void testDegreesToFirebaseRotationValid() throws Exception {
        TextRecognition recog = new TextRecognition();
        java.lang.reflect.Method m = TextRecognition.class.getDeclaredMethod("degreesToFirebaseRotation", int.class);
        m.setAccessible(true);
        assertEquals(0, m.invoke(recog, 0));
        assertEquals(1, m.invoke(recog, 90));
        assertEquals(2, m.invoke(recog, 180));
        assertEquals(3, m.invoke(recog, 270));
    }

    @Test(expected = IllegalArgumentException.class)
    public void testDegreesToFirebaseRotationInvalid() throws Exception {
        TextRecognition recog = new TextRecognition();
        java.lang.reflect.Method m = TextRecognition.class.getDeclaredMethod("degreesToFirebaseRotation", int.class);
        m.setAccessible(true);
        m.invoke(recog, 45); // Should throw
    }

    // We cannot easily mock all FirebaseVision dependencies for detect() in plain JVM/JUnit. This covers at least the public API construction and the branch logic above.
}