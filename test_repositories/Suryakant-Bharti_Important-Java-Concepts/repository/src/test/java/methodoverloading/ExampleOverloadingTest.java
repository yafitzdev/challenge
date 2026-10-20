package methodoverloading;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class ExampleOverloadingTest {

    @Test
    void testMinFunctionInt() {
        assertEquals(6, ExampleOverloading.minFunction(11, 6));
        assertEquals(-3, ExampleOverloading.minFunction(-3, 4));
        assertEquals(-5, ExampleOverloading.minFunction(-5, -2));
        assertEquals(7, ExampleOverloading.minFunction(7, 7));
    }

    @Test
    void testMinFunctionDouble() {
        assertEquals(7.3, ExampleOverloading.minFunction(7.3, 9.4), 1e-9);
        assertEquals(-5.5, ExampleOverloading.minFunction(-5.5, 0.0), 1e-9);
        assertEquals(-10.2, ExampleOverloading.minFunction(-10.2, -2.3), 1e-9);
        assertEquals(12.0, ExampleOverloading.minFunction(12.0, 12.0), 1e-9);
    }
}