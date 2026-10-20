package com.opengamma.elsql;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ContainerSqlFragmentPublicTest {

    static class DummyFragment extends SqlFragment {
        private final String tag;
        DummyFragment(String tag) { this.tag = tag; }
        @Override void toSQL(StringBuilder buf, SqlFragments fragments, SqlParams params, int[] loopIndex) {
            buf.append(tag);
        }
        @Override public String toString() { return tag; }
    }

    @Test
    void testAddAndGetFragmentsWithDifferentValues() {
        ContainerSqlFragment container = new ContainerSqlFragment();
        DummyFragment frag1 = new DummyFragment("foo");
        DummyFragment frag2 = new DummyFragment("bar");
        container.addFragment(frag1);
        container.addFragment(frag2);
        assertEquals(2, container.getFragments().size());
        assertTrue(container.getFragments().contains(frag2));
    }

    @Test
    void testToSQLCallsChildrenWithDifferentValues() {
        ContainerSqlFragment container = new ContainerSqlFragment();
        container.addFragment(new DummyFragment("Hello"));
        container.addFragment(new DummyFragment("World"));
        StringBuilder buf = new StringBuilder();
        container.toSQL(buf, null, null, new int[0]);
        assertEquals("HelloWorld", buf.toString());
    }

    @Test
    void testToStringFormatWithDifferentValues() {
        ContainerSqlFragment container = new ContainerSqlFragment();
        container.addFragment(new DummyFragment("TestingValue"));
        assertTrue(container.toString().contains("TestingValue"));
    }
}