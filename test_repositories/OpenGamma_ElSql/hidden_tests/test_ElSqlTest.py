import pytest
from src.opengamma.elsql import ElSql, ElSqlConfig, EmptySqlParams

def test_of_noOverride():
    test = ElSql.of(ElSqlConfig.DEFAULT, ElSql)
    assert test.getConfig() == ElSqlConfig.DEFAULT
    assert test.getSql("TestFoo") == "SELECT * FROM foo "
    assert test.getSql("TestBar") == "SELECT * FROM bar "

def test_of_noOverride_withConfig():
    test = ElSql.of(ElSqlConfig.DEFAULT, ElSql)
    assert test.getConfig() == ElSqlConfig.DEFAULT
    test.withConfig(ElSqlConfig.HSQL)
    assert test.getSql("TestFoo") == "SELECT * FROM foo "
    assert test.getSql("TestBar") == "SELECT * FROM bar "

def test_of_dbOverride():
    test = ElSql.of(ElSqlConfig.HSQL, ElSql)
    assert test.getSql("TestFoo") == "SELECT * FROM foo "
    assert test.getSql("TestBar") == "SELECT * FROM bar, foo "

def test_of_nullConfig():
    with pytest.raises(ValueError):
        ElSql.of(None, ElSql)

def test_of_nullClass():
    with pytest.raises(ValueError):
        ElSql.of(ElSqlConfig.DEFAULT, None)

def test_parse_nullConfig():
    with pytest.raises(ValueError):
        ElSql.parse(None, [])

def test_parse_nullClass():
    with pytest.raises(ValueError):
        ElSql.parse(ElSqlConfig.DEFAULT, None)

def test_parse_noExistingResource():
    class Dummy:
        def __init__(self, name):
            self.name = name
    resources = [Dummy("NAME_OF_NON_EXISTING_RESOURCE.elsql")]
    with pytest.raises(ValueError):
        ElSql.parse(ElSqlConfig.DEFAULT, resources)

def test_getSql():
    test = ElSql.of(ElSqlConfig.DEFAULT, ElSql)
    assert test.getSql("TestFoo") == "SELECT * FROM foo "
    assert test.getSql("TestFoo", EmptySqlParams.INSTANCE) == "SELECT * FROM foo "