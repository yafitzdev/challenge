from src.opengamma.elsql import ValueSqlFragment, SqlParams, MapSqlParams

def test_value_present_follow_with_space():
    frag = ValueSqlFragment(":foo", True)
    buf = []
    params = MapSqlParams({"foo": "bar"})
    frag.toSQL(buf, None, params, [])
    assert "".join(buf) == "bar "

def test_value_present_no_space():
    frag = ValueSqlFragment(":foo", False)
    buf = []
    params = MapSqlParams({"foo": 42})
    frag.toSQL(buf, None, params, [])
    assert "".join(buf) == "42"

def test_value_absent():
    frag = ValueSqlFragment(":foo", True)
    buf = []
    params = MapSqlParams({})
    frag.toSQL(buf, None, params, [])
    assert "".join(buf) == ""

def test_toString():
    frag = ValueSqlFragment(":foo", True)
    s = str(frag)
    assert "foo" in s
    assert s.startswith("ValueSqlFragment")