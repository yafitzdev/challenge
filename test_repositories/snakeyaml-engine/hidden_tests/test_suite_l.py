import pytest

from src.snakeyaml_engine import iter_events


def test_case_L24T_00():
    yaml = 'foo: |\n  x\n   \n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '=VAL |x\\n \\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_L24T_01():
    yaml = 'foo: |\n  x\n   '
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '=VAL |x\\n \\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_L383():
    yaml = '--- foo  # comment\n--- foo  # comment\n'
    expected = ['+STR', '+DOC ---', '=VAL :foo', '-DOC', '+DOC ---', '=VAL :foo', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_L94M():
    yaml = '? !!str a\n: !!int 47\n? c\n: !!str d\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL <tag:yaml.org,2002:str> :a', '=VAL <tag:yaml.org,2002:int> :47', '=VAL :c', '=VAL <tag:yaml.org,2002:str> :d', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_L9U5():
    yaml = 'implicit block key : [\n  implicit flow key : value,\n ]\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :implicit block key', '+SEQ []', '+MAP {}', '=VAL :implicit flow key', '=VAL :value', '-MAP', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_LE5A():
    yaml = '- !!str "a"\n- \'b\'\n- &anchor "c"\n- *anchor\n- !!str\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL <tag:yaml.org,2002:str> "a', "=VAL 'b", '=VAL &anchor "c', '=ALI *anchor', '=VAL <tag:yaml.org,2002:str> :', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_LHL4():
    yaml = '---\n!invalid{}tag scalar\n'
    expected = ['+STR', '+DOC ---']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_LP6E():
    yaml = '- [a, b , c ]\n- { "a"  : b\n   , c : \'d\' ,\n   e   : "f"\n  }\n- [      ]\n'
    expected = ['+STR', '+DOC', '+SEQ', '+SEQ []', '=VAL :a', '=VAL :b', '=VAL :c', '-SEQ', '+MAP {}', '=VAL "a', '=VAL :b', '=VAL :c', "=VAL 'd", '=VAL :e', '=VAL "f', '-MAP', '+SEQ []', '-SEQ', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_LQZ7():
    yaml = '"implicit block key" : [\n  "implicit flow key" : value,\n ]\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL "implicit block key', '+SEQ []', '+MAP {}', '=VAL "implicit flow key', '=VAL :value', '-MAP', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
