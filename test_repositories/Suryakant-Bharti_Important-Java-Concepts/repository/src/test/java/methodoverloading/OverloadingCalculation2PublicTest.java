package methodoverloading;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

class OverloadingCalculation2PublicTest {

    @Test
    void testSumIntArgs() {
        OverloadingCalculation2 obj = new OverloadingCalculation2();
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream orig = System.out;
        try {
            System.setOut(new PrintStream(out));
            obj.sum(8, 13);
            System.setOut(orig);
            assertTrue(out.toString().trim().contains("int arg method invoked"));
        } finally {
            System.setOut(orig);
        }
    }

    @Test
    void testSumLongArgs() {
        OverloadingCalculation2 obj = new OverloadingCalculation2();
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream orig = System.out;
        try {
            System.setOut(new PrintStream(out));
            obj.sum(13L, 22L);
            System.setOut(orig);
            assertTrue(out.toString().trim().contains("long arg method invoked"));
        } finally {
            System.setOut(orig);
        }
    }
}