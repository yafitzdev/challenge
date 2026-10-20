package com.github.tamir7.contacts;

import org.junit.Test;
import static org.junit.Assert.*;

public class EventTest {

    @Test
    public void testConstructorsAndGetters_Type() {
        Event e = new Event("2023-01-01", Event.Type.BIRTHDAY);
        assertEquals("2023-01-01", e.getStartDate());
        assertEquals(Event.Type.BIRTHDAY, e.getType());
        assertNull(e.getLabel());
    }

    @Test
    public void testConstructorsAndGetters_Label() {
        Event e = new Event("2023-01-01", "Anniversary");
        assertEquals("2023-01-01", e.getStartDate());
        assertEquals(Event.Type.CUSTOM, e.getType());
        assertEquals("Anniversary", e.getLabel());
    }

    @Test
    public void testEqualsAndHashCode() {
        Event e1 = new Event("2020-10-10", Event.Type.BIRTHDAY);
        Event e2 = new Event("2020-10-10", Event.Type.BIRTHDAY);
        Event e3 = new Event("2020-10-10", "CustomEvt");
        assertEquals(e1, e2);
        assertNotEquals(e1, e3);
        assertEquals(e1.hashCode(), e2.hashCode());
    }

    @Test
    public void testTypeFromValue() {
        assertEquals(Event.Type.CUSTOM, Event.Type.fromValue(0));
        assertEquals(Event.Type.ANNIVERSARY, Event.Type.fromValue(1));
        assertEquals(Event.Type.OTHER, Event.Type.fromValue(2));
        assertEquals(Event.Type.BIRTHDAY, Event.Type.fromValue(3));
        assertEquals(Event.Type.UNKNOWN, Event.Type.fromValue(99));
    }

    @Test
    public void testNotEqualConditions() {
        Event e1 = new Event("d", Event.Type.BIRTHDAY);
        assertNotEquals(e1, null);
        assertNotEquals(e1, "notAnEvent");
        Event e2 = new Event("other", Event.Type.BIRTHDAY);
        assertNotEquals(e1, e2);
    }
}