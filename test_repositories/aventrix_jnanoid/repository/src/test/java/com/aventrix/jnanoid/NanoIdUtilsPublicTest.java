package com.aventrix.jnanoid;

import org.junit.Test;
import com.aventrix.jnanoid.jnanoid.NanoIdUtils;

import java.security.SecureRandom;
import java.util.Random;

import static org.junit.Assert.*;

public class NanoIdUtilsPublicTest {

    private String charArrayToString(char[] arr) {
        return new String(arr);
    }

    @Test
    public void test_randomNanoId_noArgs_lengthAndAlphabet() {
        String nanoid = NanoIdUtils.randomNanoId();
        assertNotNull(nanoid);
        // Use the default length of 21
        assertEquals(21, nanoid.length());

        // Default alphabet
        String defaultAlphabetStr = charArrayToString(NanoIdUtils.DEFAULT_ALPHABET);
        for (char c : nanoid.toCharArray()) {
            assertTrue(defaultAlphabetStr.indexOf(c) >= 0);
        }
    }

    @Test
    public void test_randomNanoId_customAlphabet_public() {
        char[] customAlphabet = {'a', 'B', '4', '!'};
        SecureRandom random = new SecureRandom();
        int size = 13; // Different length from sample tests
        String nanoid = NanoIdUtils.randomNanoId(random, customAlphabet, size);
        assertNotNull(nanoid);
        assertEquals(size, nanoid.length());
        String alphabetString = charArrayToString(customAlphabet);
        for (char c : nanoid.toCharArray()) {
            assertTrue(alphabetString.indexOf(c) >= 0);
        }
    }

    @Test(expected = IllegalArgumentException.class)
    public void test_randomNanoId_nullAlphabet_public() {
        SecureRandom random = new SecureRandom();
        NanoIdUtils.randomNanoId(random, null, 10);
    }

    @Test(expected = IllegalArgumentException.class)
    public void test_randomNanoId_emptyAlphabet_public() {
        SecureRandom random = new SecureRandom();
        NanoIdUtils.randomNanoId(random, new char[0], 8);
    }

    @Test(expected = IllegalArgumentException.class)
    public void test_randomNanoId_tooShortLength_public() {
        char[] alphabet = {'a', 'b'};
        SecureRandom random = new SecureRandom();
        NanoIdUtils.randomNanoId(random, alphabet, 0);
    }

    @Test(expected = IllegalArgumentException.class)
    public void test_randomNanoId_negativeLength_public() {
        char[] alphabet = {'a', 'b', 'c'};
        SecureRandom random = new SecureRandom();
        NanoIdUtils.randomNanoId(random, alphabet, -5);
    }

    @Test(expected = IllegalArgumentException.class)
    public void test_randomNanoId_alphabetTooLong_public() {
        char[] alphabet = new char[300];
        for (int i = 0; i < 300; i++) alphabet[i] = (char) (32 + (i % 94)); // printable ASCII
        SecureRandom random = new SecureRandom();
        NanoIdUtils.randomNanoId(random, alphabet, 8);
    }

    @Test
    public void test_randomNanoId_customRandom_public() {
        Random predictableRandom = new Random(42L); // Use a different predictable seed than original tests
        char[] alphabet = {'Q', 'W', 'E'};
        int size = 6;
        String nanoid = NanoIdUtils.randomNanoId(predictableRandom, alphabet, size);
        assertEquals(size, nanoid.length());
        String alphabetString = charArrayToString(alphabet);
        for (char c : nanoid.toCharArray()) {
            assertTrue(alphabetString.indexOf(c) >= 0);
        }
        // Result should be deterministic for this predictableRandom + alphabet
        String expected = NanoIdUtils.randomNanoId(new Random(42L), alphabet, size);
        assertEquals(expected, nanoid);
    }

    @Test
    public void test_randomNanoId_defaultRandom_public() {
        // Use DEFAULT_ALPHABET but a different length from default for public test
        int length = 17;
        SecureRandom rnd = new SecureRandom();
        char[] defaultAlphabet = NanoIdUtils.DEFAULT_ALPHABET;
        String nanoid = NanoIdUtils.randomNanoId(rnd, defaultAlphabet, length);
        assertEquals(length, nanoid.length());
        String defaultAlphabetStr = charArrayToString(defaultAlphabet);
        for (char c : nanoid.toCharArray()) {
            assertTrue(defaultAlphabetStr.indexOf(c) >= 0);
        }
    }
}