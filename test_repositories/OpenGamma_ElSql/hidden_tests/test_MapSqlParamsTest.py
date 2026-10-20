import pytest
from src.opengamma.elsql import MapSqlParams

def test_constructor_Map():
    map = {"a": "b"}
    test = MapSqlParams(map)
    assert test.contains("a") is True
    assert test.get("a") == "b"

def test_constructor_Map_null():
    with pytest.raises(ValueError):
        MapSqlParams(None)

def test_constructor_KeyValue():
    test = MapSqlParams("a", "b")
    assert test.contains("a") is True
    assert test.get("a") == "b"

def test_with():
    test = MapSqlParams({})
    assert test.contains("a") is False
    assert test.get("a") is None
    test = test.with_("a", "b")
    assert test.contains("a") is True
    assert test.get("a") == "b"