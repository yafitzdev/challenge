package com.bmw.hmm;

import org.junit.Test;
import static org.junit.Assert.*;

public class TransitionTest {

    @Test
    public void testEqualsAndHashCode() {
        Transition<String> t1 = new Transition<>("A", "B");
        Transition<String> t2 = new Transition<>("A", "B");
        Transition<String> t3 = new Transition<>("B", "A");
        Transition<String> t4 = new Transition<>("A", "C");
        assertEquals(t1, t2);
        assertEquals(t1.hashCode(), t2.hashCode());
        assertNotEquals(t1, t3);
        assertNotEquals(t1.hashCode(), t3.hashCode());
        assertNotEquals(t1, t4);
    }

    @Test
    public void testEqualsWithNulls() {
        Transition<String> t1 = new Transition<>(null, "B");
        Transition<String> t2 = new Transition<>(null, "B");
        Transition<String> t3 = new Transition<>("A", null);
        Transition<String> t4 = new Transition<>(null, null);
        Transition<String> t5 = new Transition<>(null, null);

        assertEquals(t1, t2);
        assertEquals(t4, t5);
        assertNotEquals(t1, t3);
    }

    @Test
    public void testToString() {
        Transition<String> t = new Transition<>("A", "B");
        assertTrue(t.toString().contains("fromCandidate=A"));
        assertTrue(t.toString().contains("toCandidate=B"));
    }

    @Test
    public void testNotEqualsOtherTypesAndNull() {
        Transition<String> t = new Transition<>("A", "B");
        assertNotEquals(t, null);
        assertNotEquals(t, "not_a_transition");
    }
}