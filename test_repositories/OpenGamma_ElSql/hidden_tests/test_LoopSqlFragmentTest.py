import pytest
from src.opengamma.elsql import LoopSqlFragment, SqlFragment, MapSqlParams

class DummyFragment(SqlFragment):
    def toSQL(self, buf, fragments, params, loopIndex):
        if loopIndex:
            buf.append(str(loopIndex[-1]))
        else:
            buf.append("z")
        buf.append("@LOOPJOIN ")

    def __str__(self):
        return "d"

def test_loop_with_int_literal():
    loop = LoopSqlFragment("2")
    loop.addFragment(DummyFragment())
    buf = []
    loop.toSQL(buf, None, MapSqlParams({}), [])
    # Remove @LOOPJOIN, join to string, and check result
    assert "".join(buf).replace("@LOOPJOIN ", "") == "0 1 "

def test_loop_with_size_variable_number():
    params = MapSqlParams({"foo": 3})
    loop = LoopSqlFragment(":foo")
    class _Fragment(SqlFragment):
        def toSQL(self, buf, fragments, params, loopIndex):
            buf.append(str(loopIndex[-1]))
    loop.addFragment(_Fragment())
    buf = []
    loop.toSQL(buf, None, params, [])
    assert "".join(buf) == "012"

def test_loop_with_size_variable_string():
    params = MapSqlParams({"foo": "2"})
    loop = LoopSqlFragment(":foo")
    class _Fragment(SqlFragment):
        def toSQL(self, buf, fragments, params, loopIndex):
            buf.append('x')
    loop.addFragment(_Fragment())
    buf = []
    loop.toSQL(buf, None, params, [])
    assert "".join(buf) == "xx"

def test_loop_variable_not_found():
    loop = LoopSqlFragment(":unknown")
    loop.addFragment(DummyFragment())
    buf = []
    with pytest.raises(ValueError) as ex:
        loop.toSQL(buf, None, MapSqlParams({}), [])
    assert "Loop size variable not found" in str(ex.value)

def test_loop_variable_bad_type():
    loop = LoopSqlFragment(":foo")
    loop.addFragment(DummyFragment())
    params = MapSqlParams({"foo": object()})
    with pytest.raises(ValueError) as ex:
        loop.toSQL([], None, params, [])
    assert "must be Number or String" in str(ex.value)

def test_toString_gives_class_name():
    loop = LoopSqlFragment("2")
    assert "LoopSqlFragment" in str(loop)