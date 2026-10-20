package com.aventrix.jnanoid;

import org.junit.Test;

import com.aventrix.jnanoid.jnanoid.NanoIdUtils;

import java.security.SecureRandom;
import java.util.Random;

import static org.junit.Assert.*;

public class NanoIdUtilsTest {

    @Test
    public void testDefaultRandomNanoId() {
        String nanoid = NanoIdUtils.randomNanoId();
        assertNotNull(nanoid);
        assertEquals(NanoIdUtils.DEFAULT_SIZE, nanoid.length());
        // Should only contain characters in the default alphabet
        for (char c : nanoid.toCharArray()) {
            assertTrue(new String(NanoIdUtils.DEFAULT_ALPHABET).indexOf(c) != -1);
        }
    }

    @Test
    public void testRandomNanoIdWithCustomSize() {
        int length = 10;
        String nanoid = NanoIdUtils.randomNanoId(new SecureRandom(), NanoIdUtils.DEFAULT_ALPHABET, length);
        assertNotNull(nanoid);
        assertEquals(length, nanoid.length());
    }

    @Test
    public void testRandomNanoIdWithMinMaxSize() {
        int length = 1;
        String nanoid = NanoIdUtils.randomNanoId(new SecureRandom(), NanoIdUtils.DEFAULT_ALPHABET, length);
        assertEquals(length, nanoid.length());

        length = 1024;
        nanoid = NanoIdUtils.randomNanoId(new SecureRandom(), NanoIdUtils.DEFAULT_ALPHABET, length);
        assertEquals(length, nanoid.length());
    }

    @Test(expected = IllegalArgumentException.class)
    public void testRandomNanoIdZeroSize() {
        NanoIdUtils.randomNanoId(new SecureRandom(), NanoIdUtils.DEFAULT_ALPHABET, 0);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testRandomNanoIdNegativeSize() {
        NanoIdUtils.randomNanoId(new SecureRandom(), NanoIdUtils.DEFAULT_ALPHABET, -1);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testRandomNanoIdNullRandom() {
        NanoIdUtils.randomNanoId(null, NanoIdUtils.DEFAULT_ALPHABET, 10);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testRandomNanoIdNullAlphabet() {
        NanoIdUtils.randomNanoId(new SecureRandom(), null, 10);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testRandomNanoIdEmptyAlphabet() {
        NanoIdUtils.randomNanoId(new SecureRandom(), new char[0], 10);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testRandomNanoIdOversizedAlphabet() {
        char[] bigAlphabet = new char[256];
        for (int i = 0; i < bigAlphabet.length; i++) {
            bigAlphabet[i] = (char) ('a' + (i % 26));
        }
        NanoIdUtils.randomNanoId(new SecureRandom(), bigAlphabet, 10);
    }

    @Test
    public void testNanoIdIsUrlFriendly() {
        String nanoid = NanoIdUtils.randomNanoId();
        assertTrue(nanoid.matches("[_\\-0-9a-zA-Z]+"));
    }

    @Test
    public void testNanoIdUtilsPrivateConstructor() throws Exception {
        // Use reflection to access private constructor for coverage
        java.lang.reflect.Constructor<?> ctor = NanoIdUtils.class.getDeclaredConstructor();
        ctor.setAccessible(true);
        // Should not throw
        ctor.newInstance();
    }

    @Test
    public void testRandomNanoIdWithNonDefaultRandom() {
        Random rng = new Random(1234);
        String nanoid = NanoIdUtils.randomNanoId(rng, NanoIdUtils.DEFAULT_ALPHABET, 11);
        assertNotNull(nanoid);
        assertEquals(11, nanoid.length());
    }

    @Test
    public void testRandomNanoIdWithSmallAlphabet() {
        char[] alphabet = {'a', 'b'};
        String nanoid = NanoIdUtils.randomNanoId(new SecureRandom(), alphabet, 6);
        assertEquals(6, nanoid.length());
        for (char c : nanoid.toCharArray()) {
            assertTrue(c == 'a' || c == 'b');
        }
    }

    @Test
    public void testNanoIdUniqueness() {
        String nanoid1 = NanoIdUtils.randomNanoId();
        String nanoid2 = NanoIdUtils.randomNanoId();
        // Very low probability of equality for default size+alphabet
        assertNotEquals(nanoid1, nanoid2);
    }
}