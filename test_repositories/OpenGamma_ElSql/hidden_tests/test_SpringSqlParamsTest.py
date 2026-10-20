import pytest
from src.opengamma.elsql import SpringSqlParams, MapSqlParameterSource

def test_constructor_Map():
    source = MapSqlParameterSource()
    source.addValue("a", "b")
    test = SpringSqlParams(source)
    assert test.contains("a") is True
    assert test.get("a") == "b"
    assert test.contains("x") is False
    assert test.get("x") is None

def test_constructor_Map_null():
    with pytest.raises(ValueError):
        SpringSqlParams(None)