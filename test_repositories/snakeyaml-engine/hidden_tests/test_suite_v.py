import pytest

from src.snakeyaml_engine import iter_events


def test_case_V55R():
    yaml = '- &a a\n- &b b\n- *a\n- *b\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL &a :a', '=VAL &b :b', '=ALI *a', '=ALI *b', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_V9D5():
    yaml = '- sun: yellow\n- ? earth: blue\n  : moon: white\n'
    expected = ['+STR', '+DOC', '+SEQ', '+MAP', '=VAL :sun', '=VAL :yellow', '-MAP', '+MAP', '+MAP', '=VAL :earth', '=VAL :blue', '-MAP', '+MAP', '=VAL :moon', '=VAL :white', '-MAP', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_VJP3_00():
    yaml = 'k: {\nk\n:\nv\n}\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :k', '+MAP {}', '=VAL :k', '=VAL :']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_VJP3_01():
    yaml = 'k: {\n k\n :\n v\n }\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :k', '+MAP {}', '=VAL :k', '=VAL :']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected
