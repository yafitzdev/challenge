import pytest

from src.snakeyaml_engine import iter_events


def test_case_33X3():
    yaml = '---\n- !!int 1\n- !!int -2\n- !!int 33\n'
    expected = ['+STR', '+DOC ---', '+SEQ', '=VAL <tag:yaml.org,2002:int> :1', '=VAL <tag:yaml.org,2002:int> :-2', '=VAL <tag:yaml.org,2002:int> :33', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_35KP():
    yaml = '--- !!map\n? a\n: b\n--- !!seq\n- !!str c\n--- !!str\nd\ne\n'
    expected = ['+STR', '+DOC ---', '+MAP <tag:yaml.org,2002:map>', '=VAL :a', '=VAL :b', '-MAP', '-DOC', '+DOC ---', '+SEQ <tag:yaml.org,2002:seq>', '=VAL <tag:yaml.org,2002:str> :c', '-SEQ', '-DOC', '+DOC ---', '=VAL <tag:yaml.org,2002:str> :d e', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_36F6():
    yaml = '---\nplain: a\n b\n\n c\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :plain', '=VAL :a b\\nc', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_3ALJ():
    yaml = '- - s1_i1\n  - s1_i2\n- s2\n'
    expected = ['+STR', '+DOC', '+SEQ', '+SEQ', '=VAL :s1_i1', '=VAL :s1_i2', '-SEQ', '=VAL :s2', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_3HFZ():
    yaml = '---\nkey: value\n... invalid\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :key', '=VAL :value', '-MAP', '-DOC ...']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_3MYT():
    yaml = '---\nk:#foo\n &a !t s\n'
    expected = ['+STR', '+DOC ---', '=VAL :k:#foo &a !t s', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_3R3P():
    yaml = '&sequence\n- a\n'
    expected = ['+STR', '+DOC', '+SEQ &sequence', '=VAL :a', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_3RLN_00():
    yaml = '"1 leading\n    \\ttab"\n'
    expected = ['+STR', '+DOC', '=VAL "1 leading \\ttab', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_3RLN_01():
    yaml = '"2 leading\n    \\\ttab"\n'
    expected = ['+STR', '+DOC', '=VAL "2 leading \\ttab', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_3RLN_02():
    yaml = '"3 leading\n    \ttab"\n'
    expected = ['+STR', '+DOC', '=VAL "3 leading tab', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_3RLN_03():
    yaml = '"4 leading\n    \\t  tab"\n'
    expected = ['+STR', '+DOC', '=VAL "4 leading \\t  tab', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_3RLN_04():
    yaml = '"5 leading\n    \\\t  tab"\n'
    expected = ['+STR', '+DOC', '=VAL "5 leading \\t  tab', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_3RLN_05():
    yaml = '"6 leading\n    \t  tab"\n'
    expected = ['+STR', '+DOC', '=VAL "6 leading tab', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
