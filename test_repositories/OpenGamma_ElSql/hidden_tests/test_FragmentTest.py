import pytest
from src.opengamma.elsql import (
    NameSqlFragment, ContainerSqlFragment, IncludeSqlFragment, ValueSqlFragment, TextSqlFragment,
    EqualsSqlFragment, LikeSqlFragment, LoopSqlFragment,
    OffsetFetchSqlFragment, PagingSqlFragment, WhereSqlFragment,
    AndSqlFragment, OrSqlFragment
)

def test_NameSqlFragment():
    test = NameSqlFragment("test")
    assert str(test) == "NameSqlFragment:test []"

def test_NameSqlFragment_null():
    with pytest.raises(ValueError):
        NameSqlFragment(None)

def test_ContainerSqlFragment():
    test = ContainerSqlFragment()
    assert str(test) == "[]"

def test_IncludeSqlFragment_id():
    test = IncludeSqlFragment("test")
    assert str(test) == "IncludeSqlFragment:test"

def test_IncludeSqlFragment_var():
    test = IncludeSqlFragment(":test")
    assert str(test) == "IncludeSqlFragment::test"

def test_IncludeSqlFragment_varExtended():
    test = IncludeSqlFragment(":{test}")
    assert str(test) == "IncludeSqlFragment::{test}"

def test_IncludeSqlFragment_varExtendedDollar():
    test = IncludeSqlFragment(":${test}")
    assert str(test) == "IncludeSqlFragment::${test}"

def test_IncludeSqlFragment_null():
    with pytest.raises(ValueError):
        IncludeSqlFragment(None)

def test_ValueSqlFragment():
    test = ValueSqlFragment(":test", True)
    assert str(test) == "ValueSqlFragment:test"

def test_ValueSqlFragment_extended():
    test = ValueSqlFragment(":{test}", True)
    assert str(test) == "ValueSqlFragment:test"

def test_ValueSqlFragment_extendedDollar():
    test = ValueSqlFragment(":${test}", True)
    assert str(test) == "ValueSqlFragment:${test}"

def test_ValueSqlFragment_null():
    with pytest.raises(ValueError):
        ValueSqlFragment(None, True)

def test_TextSqlFragment_eol():
    test = TextSqlFragment("test", True)
    assert str(test) == "TextSqlFragment:test "

def test_TextSqlFragment_eol_empty():
    test = TextSqlFragment("", True)
    assert str(test) == "TextSqlFragment:"

def test_TextSqlFragment_notEol():
    test = TextSqlFragment("test", False)
    assert str(test) == "TextSqlFragment:test"

def test_TextSqlFragment_null():
    with pytest.raises(ValueError):
        TextSqlFragment(None, True)

def test_EqualsSqlFragment():
    test = EqualsSqlFragment(":test")
    assert str(test) == "EqualsSqlFragment:test []"

def test_EqualsSqlFragment_null():
    with pytest.raises(ValueError):
        EqualsSqlFragment(None)

def test_EqualsSqlFragment_notVariable():
    with pytest.raises(ValueError):
        EqualsSqlFragment("test")

def test_LikeSqlFragment():
    test = LikeSqlFragment(":test")
    assert str(test) == "LikeSqlFragment:test []"

def test_LikeSqlFragment_null():
    with pytest.raises(ValueError):
        LikeSqlFragment(None)

def test_LikeSqlFragment_notVariable():
    with pytest.raises(ValueError):
        LikeSqlFragment("test")

def test_LoopSqlFragment():
    test = LoopSqlFragment(":test")
    assert str(test) == "LoopSqlFragment []"

def test_OffsetFetchSqlFragment():
    test = OffsetFetchSqlFragment(":test")
    assert str(test) == "OffsetFetchSqlFragment []"

def test_PagingSqlFragment():
    test = PagingSqlFragment(":test", ":bar")
    assert str(test) == "PagingSqlFragment []"

def test_WhereSqlFragment():
    test = WhereSqlFragment()
    assert str(test) == "WhereSqlFragment []"

def test_AndSqlFragment():
    test = AndSqlFragment(":var", "match")
    assert test.getVariable() == "var"
    assert test.getMatchValue() == "match"
    assert str(test) == "AndSqlFragment:var []"

def test_AndSqlFragment_nullMatch():
    test = AndSqlFragment(":var", None)
    assert test.getVariable() == "var"
    assert test.getMatchValue() is None
    assert str(test) == "AndSqlFragment:var []"

def test_AndSqlFragment_nullVariable():
    with pytest.raises(ValueError):
        AndSqlFragment(None, "match")

def test_AndSqlFragment_notVariable():
    with pytest.raises(ValueError):
        AndSqlFragment("test", "match")

def test_AndSqlFragment_notVariableTooShort():
    with pytest.raises(ValueError):
        AndSqlFragment(":", "match")

def test_OrSqlFragment():
    test = OrSqlFragment(":var", "match")
    assert test.getVariable() == "var"
    assert test.getMatchValue() == "match"
    assert str(test) == "OrSqlFragment:var []"

def test_OrSqlFragment_nullMatch():
    test = OrSqlFragment(":var", None)
    assert test.getVariable() == "var"
    assert test.getMatchValue() is None
    assert str(test) == "OrSqlFragment:var []"

def test_OrSqlFragment_nullVariable():
    with pytest.raises(ValueError):
        OrSqlFragment(None, "match")

def test_OrSqlFragment_notVariable():
    with pytest.raises(ValueError):
        OrSqlFragment("test", "match")

def test_OrSqlFragment_notVariableTooShort():
    with pytest.raises(ValueError):
        OrSqlFragment(":", "match")