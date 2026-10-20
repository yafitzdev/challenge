package com.opengamma.elsql;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;

/**
 * Public test for SpringSqlParams with different data.
 */
public class SpringSqlParamsPublicTest {

  @Test
  public void test_constructor_Map_differentValues() {
    MapSqlParameterSource source = new MapSqlParameterSource();
    source.addValue("foo", 123);
    SpringSqlParams test = new SpringSqlParams(source);
    assertEquals(true, test.contains("foo"));
    assertEquals(123, test.get("foo"));
    assertEquals(false, test.contains("bar"));
    assertEquals(null, test.get("bar"));
  }

  @Test
  public void test_constructor_Map_null_source() {
    assertThrows(IllegalArgumentException.class, () -> new SpringSqlParams(null));
  }
}