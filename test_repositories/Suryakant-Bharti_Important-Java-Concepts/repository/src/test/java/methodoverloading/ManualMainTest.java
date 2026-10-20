package methodoverloading;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.*;

class ManualMainTest {

    @Test
    void testAdderMainManual() {
        // Adder has no main, but TestOverloading2.main simply calls Adder.add
        // Simulate what TestOverloading2.main() would do:
        assertEquals(22, Adder.add(11, 11));
        assertEquals(24.9, Adder.add(12.3, 12.6), 1e-9);
    }

    @Test
    void testExampleOverloadingMainManual() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream orig = System.out;
        try {
            System.setOut(new PrintStream(out));
            ExampleOverloading.main(new String[0]);
        } finally {
            System.setOut(orig);
        }
        String output = out.toString();
        assertTrue(output.contains("Minimum Value = 6"));
        assertTrue(output.contains("Minimum Value = 7.3"));
    }

    @Test
    void testOverloadingCalculation2Main() {
        OverloadingCalculation2 obj = new OverloadingCalculation2();
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream orig = System.out;
        try {
            System.setOut(new PrintStream(out));
            // This should call int version since both args are int literals
            OverloadingCalculation2.main(new String[0]);
            String output = out.toString();
            assertTrue(output.contains("int arg method invoked"));
        } finally {
            System.setOut(orig);
        }
    }
}