package com.tuenti.smsradar;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import java.util.HashMap;
import java.util.Map;

public class SharedPreferencesSmsStoragePublicTest {

    private SharedPreferencesSmsStorage storage;

    @Before
    public void setUp() {
        storage = new SharedPreferencesSmsStorage();
        storage.clearPreferences();
    }

    @Test
    public void testPutAndGetValue() {
        storage.putString("animal", "dog");
        Assert.assertEquals("dog", storage.getString("animal", ""));
    }

    @Test
    public void testOverwriteValue() {
        storage.putString("language", "Python");
        storage.putString("language", "Go");
        Assert.assertEquals("Go", storage.getString("language", ""));
    }

    @Test
    public void testGetDefaultIfNotPresent() {
        Assert.assertEquals("default", storage.getString("missing-key", "default"));
    }
}