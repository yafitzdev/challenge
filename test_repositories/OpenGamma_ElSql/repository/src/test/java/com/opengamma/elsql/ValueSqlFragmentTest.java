package com.opengamma.elsql;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ValueSqlFragmentTest {

    @Test
    void testValuePresentFollowWithSpace() {
        ValueSqlFragment frag = new ValueSqlFragment(":foo", true);
        StringBuilder buf = new StringBuilder();
        SqlParams params = new MapSqlParams(java.util.Collections.singletonMap("foo", "bar"));
        frag.toSQL(buf, null, params, new int[0]);
        assertEquals("bar ", buf.toString());
    }

    @Test
    void testValuePresentNoSpace() {
        ValueSqlFragment frag = new ValueSqlFragment(":foo", false);
        StringBuilder buf = new StringBuilder();
        SqlParams params = new MapSqlParams(java.util.Collections.singletonMap("foo", 42));
        frag.toSQL(buf, null, params, new int[0]);
        assertEquals("42", buf.toString());
    }

    @Test
    void testValueAbsent() {
        ValueSqlFragment frag = new ValueSqlFragment(":foo", true);
        StringBuilder buf = new StringBuilder();
        SqlParams params = new MapSqlParams(java.util.Collections.emptyMap());
        frag.toSQL(buf, null, params, new int[0]);
        assertEquals("", buf.toString());
    }

    @Test
    void testToString() {
        ValueSqlFragment frag = new ValueSqlFragment(":foo", true);
        assertTrue(frag.toString().contains("foo"));
        assertTrue(frag.toString().startsWith("ValueSqlFragment"));
    }
}