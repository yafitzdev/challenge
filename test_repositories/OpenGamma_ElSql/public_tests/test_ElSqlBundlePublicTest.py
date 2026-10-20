import pytest
from src.opengamma.elsql import ElSqlBundle, ElSqlConfig, ElSql

class DummyResource:
    def __init__(self, name):
        self.name = name

def test_of_noOverride_diff():
    test = ElSqlBundle.of(ElSqlConfig.DEFAULT, ElSql)
    assert test.getConfig() == ElSqlConfig.DEFAULT
    assert test.getSql("TestFoo") == "SELECT * FROM foo "
    assert test.getSql("TestBar") == "SELECT * FROM bar "
    # Different: Now test "TestBar"
    assert test.getSql("TestBar") == "SELECT * FROM bar "

def test_of_dbOverride_diff():
    test = ElSqlBundle.of(ElSqlConfig.HSQL, ElSql)
    assert test.getSql("TestFoo") == "SELECT * FROM foo "
    assert test.getSql("TestBar") == "SELECT * FROM bar, foo "

def test_of_nullClass_diff():
    with pytest.raises(ValueError):
        ElSqlBundle.of(ElSqlConfig.DEFAULT, None)

def test_parse_nullClass_diff():
    with pytest.raises(ValueError):
        ElSqlBundle.parse(ElSqlConfig.DEFAULT, None)

def test_parse_noExistingResource_diff():
    resource = DummyResource("DIFFERENT_NON_EXISTING_RESOURCE.elsql")
    with pytest.raises(ValueError):
        ElSqlBundle.parse(ElSqlConfig.DEFAULT, [resource])

def test_getSql_diff():
    test = ElSqlBundle.of(ElSqlConfig.DEFAULT, ElSql)
    assert test.getSql("TestBar") == "SELECT * FROM bar "
    from src.opengamma.elsql import MapSqlParameterSource
    assert test.getSql("TestBar", MapSqlParameterSource()) == "SELECT * FROM bar "