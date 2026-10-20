from src.opengamma.elsql import EqualsSqlFragment, MapSqlParams
import pytest

def test_value_null():
    frag = EqualsSqlFragment(":foo")
    buf = []
    params = MapSqlParams({})
    frag.toSQL(buf, None, params, [])
    assert "".join(buf) == "IS NULL "

def test_value_not_null():
    frag = EqualsSqlFragment(":foo")
    buf = []
    params = MapSqlParams({"foo": 7})
    frag.toSQL(buf, None, params, [])
    assert "".join(buf).startswith("= ")