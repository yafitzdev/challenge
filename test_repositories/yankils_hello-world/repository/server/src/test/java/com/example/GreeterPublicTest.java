package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class GreeterPublicTest {

    @Test
    void testGreetAnotherName() {
        Greeter greeter = new Greeter();
        String result = greeter.greet("Alice");
        assertEquals("Hello, Alice!", result);
    }

    @Test
    void testGreetWithDifferentName() {
        Greeter greeter = new Greeter();
        String result = greeter.greet("Charlie");
        assertEquals("Hello, Charlie!", result);
    }

    @Test
    void testGreetWithEmptyString() {
        Greeter greeter = new Greeter();
        String result = greeter.greet("");
        assertEquals("Hello, !", result);
    }

    @Test
    void testGreetWithSpecialCharacters() {
        Greeter greeter = new Greeter();
        String result = greeter.greet("@User#123");
        assertEquals("Hello, @User#123!", result);
    }
}