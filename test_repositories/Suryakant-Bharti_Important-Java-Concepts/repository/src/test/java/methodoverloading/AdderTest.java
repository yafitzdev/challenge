package methodoverloading;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class AdderTest {

    @Test
    void testAddInt() {
        assertEquals(22, Adder.add(11, 11));
        assertEquals(-8, Adder.add(-10, 2));
        assertEquals(0, Adder.add(0, 0));
    }

    @Test
    void testAddDouble() {
        assertEquals(24.9, Adder.add(12.3, 12.6), 1e-9);
        assertEquals(-4.4, Adder.add(-2.2, -2.2), 1e-9);
        assertEquals(0.0, Adder.add(0.0, 0.0), 1e-9);
    }
}