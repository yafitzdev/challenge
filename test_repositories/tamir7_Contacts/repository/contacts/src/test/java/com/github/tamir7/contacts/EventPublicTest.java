package com.github.tamir7.contacts;

import org.junit.Test;
import static org.junit.Assert.*;

public class EventPublicTest {

    @Test
    public void testConstructorsAndGetters_Type() {
        Event e = new Event("2050-12-31", Event.Type.ANNIVERSARY);
        assertEquals("2050-12-31", e.getStartDate());
        assertEquals(Event.Type.ANNIVERSARY, e.getType());
        assertNull(e.getLabel());
    }

    @Test
    public void testConstructorsAndGetters_Label() {
        Event e = new Event("2024-07-14", "Special Date");
        assertEquals("2024-07-14", e.getStartDate());
        assertEquals(Event.Type.CUSTOM, e.getType());
        assertEquals("Special Date", e.getLabel());
    }

    @Test
    public void testEqualsAndHashCode() {
        Event e1 = new Event("2000-01-01", Event.Type.OTHER);
        Event e2 = new Event("2000-01-01", Event.Type.OTHER);
        Event e3 = new Event("2000-01-01", "Anniv");
        assertEquals(e1, e2);
        assertNotEquals(e1, e3);
        assertEquals(e1.hashCode(), e2.hashCode());
    }

    @Test
    public void testTypeFromValue() {
        assertEquals(Event.Type.CUSTOM, Event.Type.fromValue(-1));
        assertEquals(Event.Type.ANNIVERSARY, Event.Type.fromValue(1));
        assertEquals(Event.Type.OTHER, Event.Type.fromValue(2));
        assertEquals(Event.Type.BIRTHDAY, Event.Type.fromValue(3));
        assertEquals(Event.Type.UNKNOWN, Event.Type.fromValue(500));
    }

    @Test
    public void testNotEqualConditions() {
        Event e1 = new Event("2029-11-11", Event.Type.OTHER);
        assertNotEquals(e1, null);
        assertNotEquals(e1, new Object());
        Event e2 = new Event("2222-02-22", Event.Type.OTHER);
        assertNotEquals(e1, e2);
    }
}