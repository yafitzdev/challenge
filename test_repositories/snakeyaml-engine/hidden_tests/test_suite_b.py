import pytest

from src.snakeyaml_engine import iter_events


def test_case_B3HG():
    yaml = '--- >\n folded\n text\n\n\n'
    expected = ['+STR', '+DOC ---', '=VAL >folded text\\n', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_BD7L():
    yaml = '- item1\n- item2\ninvalid: x\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL :item1', '=VAL :item2']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_BEC7():
    yaml = '%YAML 1.3 # Attempt parsing\n          # with a warning\n---\n"foo"\n'
    expected = ['+STR', '+DOC ---', '=VAL "foo', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_BF9H():
    yaml = '---\nplain: a\n       b # end of scalar\n       c\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :plain', '=VAL :a b']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_BS4K():
    yaml = 'word1  # comment\nword2\n'
    expected = ['+STR', '+DOC', '=VAL :word1', '-DOC']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_BU8L():
    yaml = 'key: &anchor\n !!map\n  a: b\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key', '+MAP &anchor <tag:yaml.org,2002:map>', '=VAL :a', '=VAL :b', '-MAP', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
