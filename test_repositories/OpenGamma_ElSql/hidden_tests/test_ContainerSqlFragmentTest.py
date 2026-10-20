from src.opengamma.elsql import ContainerSqlFragment, SqlFragment
import pytest

class DummyFragment(SqlFragment):
    def __init__(self, tag):
        self.tag = tag
    def toSQL(self, buf, fragments, params, loopIndex):
        buf.append(self.tag)
    def __str__(self):
        return self.tag

def test_add_and_get_fragments():
    container = ContainerSqlFragment()
    frag1 = DummyFragment("a")
    frag2 = DummyFragment("b")
    container.addFragment(frag1)
    container.addFragment(frag2)
    assert len(container.getFragments()) == 2
    assert frag1 in container.getFragments()

def test_toSQL_calls_children():
    container = ContainerSqlFragment()
    container.addFragment(DummyFragment("X"))
    container.addFragment(DummyFragment("Y"))
    buf = []
    container.toSQL(buf, None, None, [])
    assert "".join(buf) == "XY"

def test_toString_format():
    container = ContainerSqlFragment()
    container.addFragment(DummyFragment("X"))
    assert "X" in str(container)