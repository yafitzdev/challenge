import pytest

from src.snakeyaml_engine import iter_events


def test_case_Z67P():
    yaml = 'literal: |2\n  value\nfolded: !foo >1\n value\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :literal', '=VAL |value\\n', '=VAL :folded', '=VAL <!foo> >value\\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_Z9M4():
    yaml = '%TAG !e! tag:example.com,2000:app/\n---\n- !e!foo "bar"\n'
    expected = ['+STR', '+DOC ---', '+SEQ', '=VAL <tag:example.com,2000:app/foo> "bar', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_ZCZ6():
    yaml = 'a: b: c: d\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :a', '=VAL :b']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_ZF4X():
    yaml = 'Mark McGwire: {hr: 65, avg: 0.278}\nSammy Sosa: {\n    hr: 63,\n    avg: 0.288\n  }\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :Mark McGwire', '+MAP {}', '=VAL :hr', '=VAL :65', '=VAL :avg', '=VAL :0.278', '-MAP', '=VAL :Sammy Sosa', '+MAP {}', '=VAL :hr', '=VAL :63', '=VAL :avg', '=VAL :0.288', '-MAP', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_ZH7C():
    yaml = '&a a: b\nc: &d d\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL &a :a', '=VAL :b', '=VAL :c', '=VAL &d :d', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_ZK9H():
    yaml = '{ key: [[[\n  value\n ]]]\n}\n'
    expected = ['+STR', '+DOC', '+MAP {}', '=VAL :key', '+SEQ []', '+SEQ []', '+SEQ []', '=VAL :value', '-SEQ', '-SEQ', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_ZL4Z():
    yaml = "---\na: 'b': c\n"
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :a', "=VAL 'b"]
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_ZWK4():
    yaml = '---\na: 1\n? b\n&anchor c: 3\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :a', '=VAL :1', '=VAL :b', '=VAL :', '=VAL &anchor :c', '=VAL :3', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_ZXT5():
    yaml = '[ "key"\n  :value ]\n'
    expected = ['+STR', '+DOC', '+SEQ []', '=VAL "key']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected
