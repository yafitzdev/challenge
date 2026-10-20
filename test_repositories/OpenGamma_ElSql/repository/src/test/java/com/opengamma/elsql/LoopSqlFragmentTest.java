package com.opengamma.elsql;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Map;
import java.util.HashMap;

class LoopSqlFragmentTest {

    static class DummyFragment extends SqlFragment {
        @Override
        void toSQL(StringBuilder buf, SqlFragments fragments, SqlParams params, int[] loopIndex) {
            buf.append(loopIndex.length > 0 ? loopIndex[loopIndex.length-1] : "z");
            buf.append("@LOOPJOIN ");
        }
        @Override
        public String toString() { return "d"; }
    }

    @Test
    void testLoopWithIntLiteral() {
        LoopSqlFragment loop = new LoopSqlFragment("2");
        loop.addFragment(new DummyFragment());
        StringBuilder buf = new StringBuilder();
        loop.toSQL(buf, null, new MapSqlParams(Map.of()), new int[0]);
        // For i = 0 and i = 1 with join handling
        assertEquals("0 1 ", buf.toString().replaceAll("@LOOPJOIN ",""));
    }

    @Test
    void testLoopWithSizeVariableNumber() {
        MapSqlParams params = new MapSqlParams(Map.of("foo", 3));
        LoopSqlFragment loop = new LoopSqlFragment(":foo");
        loop.addFragment(new SqlFragment() {
            @Override
            void toSQL(StringBuilder buf, SqlFragments fragments, SqlParams params, int[] loopIndex) {
                buf.append(loopIndex[loopIndex.length-1]);
            }
        });
        StringBuilder buf = new StringBuilder();
        loop.toSQL(buf, null, params, new int[0]);
        assertEquals("012", buf.toString());
    }

    @Test
    void testLoopWithSizeVariableString() {
        MapSqlParams params = new MapSqlParams(Map.of("foo", "2"));
        LoopSqlFragment loop = new LoopSqlFragment(":foo");
        loop.addFragment(new SqlFragment() {
            @Override
            void toSQL(StringBuilder buf, SqlFragments fragments, SqlParams params, int[] loopIndex) {
                buf.append('x');
            }
        });
        StringBuilder buf = new StringBuilder();
        loop.toSQL(buf, null, params, new int[0]);
        assertEquals("xx", buf.toString());
    }

    @Test
    void testLoopVariableNotFound() {
        LoopSqlFragment loop = new LoopSqlFragment(":unknown");
        // add dummy
        loop.addFragment(new DummyFragment());
        StringBuilder buf = new StringBuilder();
        Exception ex = assertThrows(IllegalArgumentException.class, () ->
            loop.toSQL(buf, null, new MapSqlParams(Map.of()), new int[0]));
        assertTrue(ex.getMessage().contains("Loop size variable not found"));
    }

    @Test
    void testLoopVariableBadType() {
        LoopSqlFragment loop = new LoopSqlFragment(":foo");
        loop.addFragment(new DummyFragment());
        MapSqlParams params = new MapSqlParams(Map.of("foo", new Object()));
        Exception ex = assertThrows(IllegalArgumentException.class, () ->
            loop.toSQL(new StringBuilder(), null, params, new int[0]));
        assertTrue(ex.getMessage().contains("must be Number or String"));
    }

    @Test
    void testToStringGivesClassName() {
        LoopSqlFragment loop = new LoopSqlFragment("2");
        assertTrue(loop.toString().contains("LoopSqlFragment"));
    }
}