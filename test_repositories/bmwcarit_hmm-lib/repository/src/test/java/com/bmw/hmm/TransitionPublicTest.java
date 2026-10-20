package com.bmw.hmm;

import org.junit.Test;
import static org.junit.Assert.*;

public class TransitionPublicTest {

    @Test
    public void testEqualsAndHashCodePublic() {
        Transition<String> t1 = new Transition<>("X", "Y");
        Transition<String> t2 = new Transition<>("X", "Y");
        Transition<String> t3 = new Transition<>("Y", "Z");
        Transition<String> t4 = new Transition<>("X", "Z");
        assertEquals(t1, t2);
        assertEquals(t1.hashCode(), t2.hashCode());
        assertNotEquals(t1, t3);
        assertNotEquals(t1.hashCode(), t3.hashCode());
        assertNotEquals(t1, t4);
    }

    @Test
    public void testEqualsWithNullsPublic() {
        Transition<String> t1 = new Transition<>(null, "Y");
        Transition<String> t2 = new Transition<>(null, "Y");
        Transition<String> t3 = new Transition<>("X", null);
        Transition<String> t4 = new Transition<>(null, null);
        Transition<String> t5 = new Transition<>(null, null);

        assertEquals(t1, t2);
        assertEquals(t4, t5);
        assertNotEquals(t1, t3);
    }

    @Test
    public void testToStringPublic() {
        Transition<String> t = new Transition<>("Q", "P");
        assertTrue(t.toString().contains("fromCandidate=Q"));
        assertTrue(t.toString().contains("toCandidate=P"));
    }

    @Test
    public void testNotEqualsOtherTypesAndNullPublic() {
        Transition<String> t = new Transition<>("I", "J");
        assertNotEquals(t, null);
        assertNotEquals(t, 12345);
    }
}