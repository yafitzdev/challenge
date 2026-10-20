from src.opengamma.elsql import ContainerSqlFragment, SqlFragment
import pytest

class DummyFragment(SqlFragment):
    def __init__(self, tag):
        self.tag = tag
    def toSQL(self, buf, fragments, params, loopIndex):
        buf.append(self.tag)
    def __str__(self):
        return self.tag

def test_add_and_get_fragments_with_different_values():
    container = ContainerSqlFragment()
    frag1 = DummyFragment("foo")
    frag2 = DummyFragment("bar")
    container.addFragment(frag1)
    container.addFragment(frag2)
    assert len(container.getFragments()) == 2
    assert frag2 in container.getFragments()

def test_toSQL_calls_children_with_different_values():
    container = ContainerSqlFragment()
    container.addFragment(DummyFragment("Hello"))
    container.addFragment(DummyFragment("World"))
    buf = []
    container.toSQL(buf, None, None, [])
    assert "".join(buf) == "HelloWorld"

def test_toString_format_with_different_values():
    container = ContainerSqlFragment()
    container.addFragment(DummyFragment("TestingValue"))
    assert "TestingValue" in str(container)