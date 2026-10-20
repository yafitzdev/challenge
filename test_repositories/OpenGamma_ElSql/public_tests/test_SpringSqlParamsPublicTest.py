import pytest
from src.opengamma.elsql import SpringSqlParams, MapSqlParameterSource

def test_constructor_Map_differentValues():
    source = MapSqlParameterSource()
    source.addValue("foo", 123)
    test = SpringSqlParams(source)
    assert test.contains("foo") is True
    assert test.get("foo") == 123
    assert test.contains("bar") is False
    assert test.get("bar") is None

def test_constructor_Map_null_source():
    with pytest.raises(ValueError):
        SpringSqlParams(None)