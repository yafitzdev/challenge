import org.junit.jupiter.api.Test;
import java.io.*;

import static org.junit.jupiter.api.Assertions.*;

public class ConvertTest {

    @Test
    public void testMainWithNumericInput() throws Exception {
        String input = "10\n";
        InputStream originalIn = System.in;
        PrintStream originalOut = System.out;
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        System.setIn(new ByteArrayInputStream(input.getBytes()));
        System.setOut(new PrintStream(outputStream));

        // try running main
        try {
            Convert.main(new String[0]);
        } catch (Exception e) {
            // ignore, just in case for input mismatch
        } finally {
            System.setIn(originalIn);
            System.setOut(originalOut);
        }
        String output = outputStream.toString();
        assertTrue(output.toLowerCase().contains("miles"), "Prompt or output should mention miles");
        assertTrue(output.toLowerCase().contains("kilometers"), "Output should mention kilometers");
    }

    @Test
    public void testMainWithInvalidInput() throws Exception {
        String input = "foo\n";
        InputStream originalIn = System.in;
        PrintStream originalOut = System.out;
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        System.setIn(new ByteArrayInputStream(input.getBytes()));
        System.setOut(new PrintStream(outputStream));
        try {
            Convert.main(new String[0]);
        } catch (Exception ignored) {
        } finally {
            System.setIn(originalIn);
            System.setOut(originalOut);
        }
        String output = outputStream.toString();
        assertTrue(output.toLowerCase().contains("miles"), "Should prompt for miles even on bad input");
    }
}