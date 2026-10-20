import pytest

from src.snakeyaml_engine import iter_events


def test_case_K3WX():
    yaml = '---\n{ "foo" # comment\n  :bar }\n'
    expected = ['+STR', '+DOC ---', '+MAP {}', '=VAL "foo', '=VAL :']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_K527():
    yaml = '>-\n  trimmed\n  \n \n\n  as\n  space\n'
    expected = ['+STR', '+DOC', '=VAL >trimmed\\n\\n\\nas space', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_K54U():
    yaml = '---\tscalar\n'
    expected = ['+STR', '+DOC ---', '=VAL :scalar', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_K858():
    yaml = 'strip: >-\n\nclip: >\n\nkeep: |+\n\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :strip', '=VAL >', '=VAL :clip', '=VAL >', '=VAL :keep', '=VAL |\\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_KH5V_00():
    yaml = '"1 inline\\ttab"\n'
    expected = ['+STR', '+DOC', '=VAL "1 inline\\ttab', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_KH5V_01():
    yaml = '"2 inline\\\ttab"\n'
    expected = ['+STR', '+DOC', '=VAL "2 inline\\ttab', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_KH5V_02():
    yaml = '"3 inline\ttab"\n'
    expected = ['+STR', '+DOC', '=VAL "3 inline\\ttab', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_KK5P():
    yaml = 'complex1:\n  ? - a\ncomplex2:\n  ? - a\n  : b\ncomplex3:\n  ? - a\n  : >\n    b\ncomplex4:\n  ? >\n    a\n  :\ncomplex5:\n  ? - a\n  : - b\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :complex1', '+MAP', '+SEQ', '=VAL :a', '-SEQ', '=VAL :', '-MAP', '=VAL :complex2', '+MAP', '+SEQ', '=VAL :a', '-SEQ', '=VAL :b', '-MAP', '=VAL :complex3', '+MAP', '+SEQ', '=VAL :a', '-SEQ', '=VAL >b\\n', '-MAP', '=VAL :complex4', '+MAP', '=VAL >a\\n', '=VAL :', '-MAP', '=VAL :complex5', '+MAP', '+SEQ', '=VAL :a', '-SEQ', '+SEQ', '=VAL :b', '-SEQ', '-MAP', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_KMK3():
    yaml = 'foo:\n  bar: 1\nbaz: 2\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '+MAP', '=VAL :bar', '=VAL :1', '-MAP', '=VAL :baz', '=VAL :2', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_KS4U():
    yaml = '---\n[\nsequence item\n]\ninvalid item\n'
    expected = ['+STR', '+DOC ---', '+SEQ []', '=VAL :sequence item', '-SEQ', '-DOC']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected
