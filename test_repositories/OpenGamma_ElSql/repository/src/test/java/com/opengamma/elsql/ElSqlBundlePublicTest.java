package com.opengamma.elsql;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;

/**
 * Public test with different data for ElSqlBundle.
 */
public class ElSqlBundlePublicTest {

  @Test
  public void test_of_noOverride_diff() {
    ElSqlBundle test = ElSqlBundle.of(ElSqlConfig.DEFAULT, ElSql.class);
    assertEquals(ElSqlConfig.DEFAULT, test.getConfig());
    assertEquals("SELECT * FROM foo ", test.getSql("TestFoo")); // The SQL file test cases depend on ElSql.elsql, must not conflict!
    assertEquals("SELECT * FROM bar ", test.getSql("TestBar"));
    // Different: Now test "TestBar"
    assertEquals("SELECT * FROM bar ", test.getSql("TestBar"));
  }

  @Test
  public void test_of_dbOverride_diff() {
    ElSqlBundle test = ElSqlBundle.of(ElSqlConfig.HSQL, ElSql.class);
    assertEquals("SELECT * FROM foo ", test.getSql("TestFoo"));
    assertEquals("SELECT * FROM bar, foo ", test.getSql("TestBar"));
  }

  @Test
  public void test_of_nullClass_diff() {
    assertThrows(IllegalArgumentException.class, () -> ElSqlBundle.of(ElSqlConfig.DEFAULT, null));
  }

  @Test
  public void test_parse_nullClass_diff() {
    assertThrows(IllegalArgumentException.class, () -> ElSqlBundle.parse(ElSqlConfig.DEFAULT, (Resource[]) null));
  }

  @Test
  public void test_parse_noExistingResource_diff() {
    Resource resource = new ClassPathResource("DIFFERENT_NON_EXISTING_RESOURCE.elsql");
    assertThrows(IllegalArgumentException.class, () -> ElSqlBundle.parse(ElSqlConfig.DEFAULT, resource));
  }

  @Test
  public void test_getSql_diff() {
    ElSqlBundle test = ElSqlBundle.of(ElSqlConfig.DEFAULT, ElSql.class);
    assertEquals("SELECT * FROM bar ", test.getSql("TestBar"));
    assertEquals("SELECT * FROM bar ", test.getSql("TestBar", new MapSqlParameterSource()));
  }

}