package methodoverloading;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class AdderPublicTest {

    @Test
    void testAddInt() {
        assertEquals(17, Adder.add(9, 8));
        assertEquals(25, Adder.add(15, 10));
        assertEquals(-6, Adder.add(-3, -3));
    }

    @Test
    void testAddDouble() {
        assertEquals(21.1, Adder.add(9.5, 11.6), 1e-9);
        assertEquals(0.0, Adder.add(-7.7, 7.7), 1e-9);
        assertEquals(-6.6, Adder.add(-2.2, -4.4), 1e-9);
    }
}