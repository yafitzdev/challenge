import org.junit.jupiter.api.Test;
import java.io.*;

import static org.junit.jupiter.api.Assertions.*;

public class HelloGoodbyeTest {

    @Test
    public void testHelloOutput() throws Exception {
        PrintStream originalOut = System.out;
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        System.setOut(new PrintStream(baos));
        Hello.main(new String[] {});
        System.setOut(originalOut);
        String output = baos.toString().trim();
        assertEquals("Hello, World!", output);
    }

    @Test
    public void testGoodbyeOutput() throws Exception {
        PrintStream originalOut = System.out;
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        System.setOut(new PrintStream(baos));
        Goodbye.main(new String[] {});
        System.setOut(originalOut);
        String output = baos.toString().replace("\r", "").trim();
        assertEquals("Goodbye, cruel world", output);
    }
}