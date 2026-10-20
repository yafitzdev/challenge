package app.arcopypaste.research.prototypes.text;

import static org.junit.Assert.*;

import org.junit.Test;
import org.mockito.Mockito;

public class TextRecognitionPublicTest {

    @Test
    public void testDegreesToFirebaseRotationValidPublic() throws Exception {
        TextRecognition recog = new TextRecognition();
        java.lang.reflect.Method m = TextRecognition.class.getDeclaredMethod("degreesToFirebaseRotation", int.class);
        m.setAccessible(true);
        assertEquals(0, m.invoke(recog, 0));
        assertEquals(1, m.invoke(recog, 90));
        assertEquals(2, m.invoke(recog, 180));
        // Changing the order, still using 3 but covering same cases:
        assertEquals(3, m.invoke(recog, 270));
    }

    @Test(expected = IllegalArgumentException.class)
    public void testDegreesToFirebaseRotationInvalidPublic() throws Exception {
        TextRecognition recog = new TextRecognition();
        java.lang.reflect.Method m = TextRecognition.class.getDeclaredMethod("degreesToFirebaseRotation", int.class);
        m.setAccessible(true);
        m.invoke(recog, 135); // Different invalid value, should still throw
    }
}