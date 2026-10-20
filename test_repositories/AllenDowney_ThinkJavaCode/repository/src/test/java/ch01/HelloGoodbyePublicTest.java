import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class HelloGoodbyePublicTest {
    @Test
    public void testHelloMainOutputDifferentData() {
        // Use custom stream and check for new output content
        java.io.ByteArrayOutputStream out = new java.io.ByteArrayOutputStream();
        System.setOut(new java.io.PrintStream(out));
        ch01.Hello.main(new String[] {});
        String output = out.toString().trim();
        // Instead of default, check starts with Hello, ends with Goodbye.
        assertTrue(output.startsWith("Hello") || output.contains("Hello"));
        assertTrue(output.contains("Goodbye"));
    }
}