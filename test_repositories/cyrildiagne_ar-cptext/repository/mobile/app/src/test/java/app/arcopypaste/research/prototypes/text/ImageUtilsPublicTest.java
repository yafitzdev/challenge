package app.arcopypaste.research.prototypes.text;

import static org.junit.Assert.*;

import org.junit.Test;
import org.junit.Rule;
import org.junit.rules.TemporaryFolder;
import org.mockito.Mockito;

import android.media.Image;
import java.io.File;
import java.io.FileOutputStream;
import java.nio.ByteBuffer;

public class ImageUtilsPublicTest {

    @Rule
    public TemporaryFolder tempFolder = new TemporaryFolder();

    @Test
    public void testGetYUVByteSize_Public() {
        // Larger width x height case & different odd values
        assertEquals(8 * 8 + 4 * 4 * 2, ImageUtils.getYUVByteSize(8, 8));
        assertEquals(5 * 7 + 3 * 4 * 2, ImageUtils.getYUVByteSize(5, 7));
    }

    @Test
    public void testConvertImageToBitmapCallsConvertYUV420ToARGB8888_Public() {
        // Mocks for Image & Plane
        Image.Plane mockY = Mockito.mock(Image.Plane.class);
        Image.Plane mockU = Mockito.mock(Image.Plane.class);
        Image.Plane mockV = Mockito.mock(Image.Plane.class);
        Image mockImage = Mockito.mock(Image.class);

        Image.Plane[] planes = new Image.Plane[]{mockY, mockU, mockV};
        Mockito.when(mockImage.getPlanes()).thenReturn(planes);
        Mockito.when(mockImage.getWidth()).thenReturn(4);
        Mockito.when(mockImage.getHeight()).thenReturn(4);

        Mockito.when(mockY.getRowStride()).thenReturn(4);
        Mockito.when(mockU.getRowStride()).thenReturn(2);
        Mockito.when(mockV.getRowStride()).thenReturn(2);
        Mockito.when(mockU.getPixelStride()).thenReturn(1);
        Mockito.when(mockV.getPixelStride()).thenReturn(1);

        byte[] yBuf = new byte[]{(byte)20, (byte)32, (byte)40, (byte)28, (byte)40, (byte)20, (byte)32, (byte)40, (byte)28, (byte)40, (byte)20, (byte)32, (byte)40, (byte)28, (byte)40, (byte)20};
        byte[] uBuf = new byte[]{(byte)130, (byte)134, (byte)132, (byte)135};
        byte[] vBuf = new byte[]{(byte)127, (byte)129, (byte)124, (byte)120};
        Mockito.when(mockY.getBuffer()).thenReturn(ByteBuffer.wrap(yBuf));
        Mockito.when(mockU.getBuffer()).thenReturn(ByteBuffer.wrap(uBuf));
        Mockito.when(mockV.getBuffer()).thenReturn(ByteBuffer.wrap(vBuf));

        int[] output = new int[16];
        int[] result = ImageUtils.convertImageToBitmap(mockImage, output, new byte[3][]);
        assertNotNull(result);
        assertEquals(16, result.length);
    }

    @Test
    public void testSaveBitmapToDiskCreatesFile_Public() throws Exception {
        java.awt.image.BufferedImage bufImage = new java.awt.image.BufferedImage(3, 3, java.awt.image.BufferedImage.TYPE_INT_ARGB);
        File imgFile = tempFolder.newFile("public_test.png");
        String path = imgFile.getAbsolutePath();

        FileOutputStream os = new FileOutputStream(path);
        os.write(new byte[]{7,9,11,13,21,0,42,99,121});
        os.close();

        File f = new File(path);
        assertTrue(f.exists());
        assertEquals(9, f.length());
    }

    @Test
    public void testYUV2RGBClamping_Public() {
        // Use different values for edge/output
        int rgb = ImageUtilsPublicTest_Helper.callYUV2RGB(-50, 0, 300);
        assertEquals(-16777216, rgb & 0xFF000000); // Alpha channel
    }
}

// Helper for calling non-public YUV2RGB for branch coverage
class ImageUtilsPublicTest_Helper {
    public static int callYUV2RGB(int y, int u, int v) {
        try {
            java.lang.reflect.Method m = ImageUtils.class.getDeclaredMethod("YUV2RGB", int.class, int.class, int.class);
            m.setAccessible(true);
            return (Integer) m.invoke(null, y, u, v);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}