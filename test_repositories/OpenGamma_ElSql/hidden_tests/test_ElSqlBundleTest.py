import pytest
from src.opengamma.elsql import ElSqlBundle, ElSqlConfig, ElSql, MapSqlParameterSource

class DummyResource:
    def __init__(self, name):
        self.name = name

def test_of_noOverride():
    test = ElSqlBundle.of(ElSqlConfig.DEFAULT, ElSql)
    assert test.getConfig() == ElSqlConfig.DEFAULT
    assert test.getSql("TestFoo") == "SELECT * FROM foo "
    assert test.getSql("TestBar") == "SELECT * FROM bar "

def test_of_noOverride_withConfig():
    test = ElSqlBundle.of(ElSqlConfig.DEFAULT, ElSql)
    assert test.getConfig() == ElSqlConfig.DEFAULT
    test.withConfig(ElSqlConfig.HSQL)  # resources not reloaded
    assert test.getSql("TestFoo") == "SELECT * FROM foo "
    assert test.getSql("TestBar") == "SELECT * FROM bar "

def test_of_dbOverride():
    test = ElSqlBundle.of(ElSqlConfig.HSQL, ElSql)
    assert test.getSql("TestFoo") == "SELECT * FROM foo "
    assert test.getSql("TestBar") == "SELECT * FROM bar, foo "

def test_of_nullConfig():
    with pytest.raises(ValueError):
        ElSqlBundle.of(None, ElSqlBundle)

def test_of_nullClass():
    with pytest.raises(ValueError):
        ElSqlBundle.of(ElSqlConfig.DEFAULT, None)

def test_parse_nullConfig():
    with pytest.raises(ValueError):
        ElSqlBundle.parse(None, [])

def test_parse_nullClass():
    with pytest.raises(ValueError):
        ElSqlBundle.parse(ElSqlConfig.DEFAULT, None)

def test_parse_noExistingResource():
    resource = DummyResource("NAME_OF_NON_EXISTING_RESOURCE.elsql")
    with pytest.raises(ValueError):
        ElSqlBundle.parse(ElSqlConfig.DEFAULT, [resource])

def test_getSql():
    test = ElSqlBundle.of(ElSqlConfig.DEFAULT, ElSql)
    assert test.getSql("TestFoo") == "SELECT * FROM foo "
    assert test.getSql("TestFoo", MapSqlParameterSource()) == "SELECT * FROM foo "