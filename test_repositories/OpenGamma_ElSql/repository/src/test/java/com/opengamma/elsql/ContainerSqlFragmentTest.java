package com.opengamma.elsql;

import org.junit.jupiter.api.Test;
import java.util.Collections;
import static org.junit.jupiter.api.Assertions.*;

class ContainerSqlFragmentTest {

    static class DummyFragment extends SqlFragment {
        private final String tag;
        DummyFragment(String tag) { this.tag = tag; }
        @Override void toSQL(StringBuilder buf, SqlFragments fragments, SqlParams params, int[] loopIndex) {
            buf.append(tag);
        }
        @Override public String toString() { return tag; }
    }

    @Test
    void testAddAndGetFragments() {
        ContainerSqlFragment container = new ContainerSqlFragment();
        DummyFragment frag1 = new DummyFragment("a");
        DummyFragment frag2 = new DummyFragment("b");
        container.addFragment(frag1);
        container.addFragment(frag2);
        assertEquals(2, container.getFragments().size());
        assertTrue(container.getFragments().contains(frag1));
    }

    @Test
    void testToSQLCallsChildren() {
        ContainerSqlFragment container = new ContainerSqlFragment();
        container.addFragment(new DummyFragment("X"));
        container.addFragment(new DummyFragment("Y"));
        StringBuilder buf = new StringBuilder();
        container.toSQL(buf, null, null, new int[0]);
        assertEquals("XY", buf.toString());
    }

    @Test
    void testToStringFormat() {
        ContainerSqlFragment container = new ContainerSqlFragment();
        container.addFragment(new DummyFragment("X"));
        assertTrue(container.toString().contains("X"));
    }
}