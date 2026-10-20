import pytest

from src.snakeyaml_engine import iter_events


def test_case_A2M4():
    yaml = '? a\n: -\tb\n  -  -\tc\n     - d\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :a', '+SEQ', '=VAL :b', '+SEQ', '=VAL :c', '=VAL :d', '-SEQ', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_A6F9():
    yaml = 'strip: |-\n  text\nclip: |\n  text\nkeep: |+\n  text\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :strip', '=VAL |text', '=VAL :clip', '=VAL |text\\n', '=VAL :keep', '=VAL |text\\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_A984():
    yaml = 'a: b\n c\nd:\n e\n  f\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :a', '=VAL :b c', '=VAL :d', '=VAL :e f', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_AB8U():
    yaml = '- single multiline\n - sequence entry\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL :single multiline - sequence entry', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_AVM7():
    yaml = ''
    expected = ['+STR', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_AZ63():
    yaml = 'one:\n- 2\n- 3\nfour: 5\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :one', '+SEQ', '=VAL :2', '=VAL :3', '-SEQ', '=VAL :four', '=VAL :5', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_AZW3():
    yaml = '- bla"keks: foo\n- bla]keks: foo\n'
    expected = ['+STR', '+DOC', '+SEQ', '+MAP', '=VAL :bla"keks', '=VAL :foo', '-MAP', '+MAP', '=VAL :bla]keks', '=VAL :foo', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
