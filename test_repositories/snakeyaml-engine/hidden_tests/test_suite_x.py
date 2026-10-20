import pytest

from src.snakeyaml_engine import iter_events


def test_case_X38W():
    yaml = '{ &a [a, &b b]: *b, *a : [c, *b, d]}\n'
    expected = ['+STR', '+DOC', '+MAP {}', '+SEQ [] &a', '=VAL :a', '=VAL &b :b', '-SEQ', '=ALI *b', '=ALI *a', '+SEQ []', '=VAL :c', '=ALI *b', '=VAL :d', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_X4QW():
    yaml = 'block: ># comment\n  scalar\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :block']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_X8DW():
    yaml = '---\n? key\n# comment\n: value\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :key', '=VAL :value', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_XLQ9():
    yaml = '---\nscalar\n%YAML 1.2\n'
    expected = ['+STR', '+DOC ---', '=VAL :scalar %YAML 1.2', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_XV9V():
    yaml = 'Folding:\n  "Empty line\n\n  as a line feed"\nChomping: |\n  Clipped empty lines\n \n\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :Folding', '=VAL "Empty line\\nas a line feed', '=VAL :Chomping', '=VAL |Clipped empty lines\\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_XW4D():
    yaml = 'a: "double\n  quotes" # lala\nb: plain\n value  # lala\nc  : #lala\n  d\n? # lala\n - seq1\n: # lala\n - #lala\n  seq2\ne:\n &node # lala\n - x: y\nblock: > # lala\n  abcde\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :a', '=VAL "double quotes', '=VAL :b', '=VAL :plain value', '=VAL :c', '=VAL :d', '+SEQ', '=VAL :seq1', '-SEQ', '+SEQ', '=VAL :seq2', '-SEQ', '=VAL :e', '+SEQ &node', '+MAP', '=VAL :x', '=VAL :y', '-MAP', '-SEQ', '=VAL :block', '=VAL >abcde\\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
