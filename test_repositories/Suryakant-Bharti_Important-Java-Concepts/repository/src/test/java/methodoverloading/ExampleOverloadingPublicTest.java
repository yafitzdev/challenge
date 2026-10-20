package methodoverloading;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class ExampleOverloadingPublicTest {

    @Test
    void testMinFunctionInt() {
        assertEquals(2, ExampleOverloading.minFunction(5, 2));
        assertEquals(-7, ExampleOverloading.minFunction(-7, 9));
        assertEquals(-20, ExampleOverloading.minFunction(-15, -20));
        assertEquals(0, ExampleOverloading.minFunction(0, 0));
    }

    @Test
    void testMinFunctionDouble() {
        assertEquals(3.2, ExampleOverloading.minFunction(8.7, 3.2), 1e-9);
        assertEquals(-9.8, ExampleOverloading.minFunction(-9.8, 4.5), 1e-9);
        assertEquals(-11.3, ExampleOverloading.minFunction(-11.3, -6.5), 1e-9);
        assertEquals(-7.7, ExampleOverloading.minFunction(-7.7, -7.7), 1e-9);
    }
}