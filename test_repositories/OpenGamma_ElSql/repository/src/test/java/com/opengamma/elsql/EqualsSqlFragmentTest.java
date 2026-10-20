package com.opengamma.elsql;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class EqualsSqlFragmentTest {

    @Test
    void testValueNull() {
        EqualsSqlFragment frag = new EqualsSqlFragment(":foo");
        StringBuilder buf = new StringBuilder();
        MapSqlParams params = new MapSqlParams(java.util.Collections.emptyMap());
        frag.toSQL(buf, null, params, new int[0]);
        assertEquals("IS NULL ", buf.toString());
    }

    @Test
    void testValueNotNull() {
        EqualsSqlFragment frag = new EqualsSqlFragment(":foo");
        StringBuilder buf = new StringBuilder();
        MapSqlParams params = new MapSqlParams(java.util.Collections.singletonMap("foo", 7));
        frag.toSQL(buf, null, params, new int[0]);
        assertTrue(buf.toString().startsWith("= "));
    }
}