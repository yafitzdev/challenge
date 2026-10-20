package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestGreeter {

    @Test
    void testGreetNormal() {
        Greeter greeter = new Greeter();
        String result = greeter.greet("World");
        assertEquals("Hello, World!", result);
    }

    @Test
    void testGreetEmpty() {
        Greeter greeter = new Greeter();
        String result = greeter.greet("");
        assertEquals("Hello, !", result);
    }

    @Test
    void testGreetWhitespace() {
        Greeter greeter = new Greeter();
        String result = greeter.greet("   ");
        assertEquals("Hello,    !", result);
    }

    @Test
    void testGreetNull() {
        Greeter greeter = new Greeter();
        // The tested code does NOT throw NPE, so just assert correct handling
        String result = greeter.greet(null);
        assertEquals("Hello, null!", result);
    }

    @Test
    void testGreetCustomName() {
        Greeter greeter = new Greeter();
        String result = greeter.greet("Alice");
        assertEquals("Hello, Alice!", result);
    }
}