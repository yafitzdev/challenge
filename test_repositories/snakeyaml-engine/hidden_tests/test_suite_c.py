import pytest

from src.snakeyaml_engine import iter_events


def test_case_C2DT():
    yaml = '{\n"adjacent":value,\n"readable": value,\n"empty":\n}\n'
    expected = ['+STR', '+DOC', '+MAP {}', '=VAL "adjacent', '=VAL :value', '=VAL "readable', '=VAL :value', '=VAL "empty', '=VAL :', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_C2SP():
    yaml = '[23\n]: 42\n'
    expected = ['+STR', '+DOC', '+SEQ []', '=VAL :23']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_C4HZ():
    yaml = '%TAG ! tag:clarkevans.com,2002:\n--- !shape\n  # Use the ! handle for presenting\n  # tag:clarkevans.com,2002:circle\n- !circle\n  center: &ORIGIN {x: 73, y: 129}\n  radius: 7\n- !line\n  start: *ORIGIN\n  finish: { x: 89, y: 102 }\n- !label\n  start: *ORIGIN\n  color: 0xFFEEBB\n  text: Pretty vector drawing.\n'
    expected = ['+STR', '+DOC ---', '+SEQ <tag:clarkevans.com,2002:shape>', '+MAP <tag:clarkevans.com,2002:circle>', '=VAL :center', '+MAP {} &ORIGIN', '=VAL :x', '=VAL :73', '=VAL :y', '=VAL :129', '-MAP', '=VAL :radius', '=VAL :7', '-MAP', '+MAP <tag:clarkevans.com,2002:line>', '=VAL :start', '=ALI *ORIGIN', '=VAL :finish', '+MAP {}', '=VAL :x', '=VAL :89', '=VAL :y', '=VAL :102', '-MAP', '-MAP', '+MAP <tag:clarkevans.com,2002:label>', '=VAL :start', '=ALI *ORIGIN', '=VAL :color', '=VAL :0xFFEEBB', '=VAL :text', '=VAL :Pretty vector drawing.', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_CC74():
    yaml = '%TAG !e! tag:example.com,2000:app/\n---\n!e!foo "bar"\n'
    expected = ['+STR', '+DOC ---', '=VAL <tag:example.com,2000:app/foo> "bar', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_CML9():
    yaml = 'key: [ word1\n#  xxx\n  word2 ]\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key', '+SEQ []', '=VAL :word1']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_CN3R():
    yaml = '&flowseq [\n a: b,\n &c c: d,\n { &e e: f },\n &g { g: h }\n]\n'
    expected = ['+STR', '+DOC', '+SEQ [] &flowseq', '+MAP {}', '=VAL :a', '=VAL :b', '-MAP', '+MAP {}', '=VAL &c :c', '=VAL :d', '-MAP', '+MAP {}', '=VAL &e :e', '=VAL :f', '-MAP', '+MAP {} &g', '=VAL :g', '=VAL :h', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_CPZ3():
    yaml = '---\ntab: "\\tstring"\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :tab', '=VAL "\\tstring', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_CQ3W():
    yaml = '---\nkey: "missing closing quote\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :key']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_CT4Q():
    yaml = '[\n? foo\n bar : baz\n]\n'
    expected = ['+STR', '+DOC', '+SEQ []', '+MAP {}', '=VAL :foo bar', '=VAL :baz', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_CTN5():
    yaml = '---\n[ a, b, c, , ]\n'
    expected = ['+STR', '+DOC ---', '+SEQ []', '=VAL :a', '=VAL :b', '=VAL :c']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_CUP7():
    yaml = 'anchored: !local &anchor value\nalias: *anchor\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :anchored', '=VAL &anchor <!local> :value', '=VAL :alias', '=ALI *anchor', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_CVW2():
    yaml = '---\n[ a, b, c,#invalid\n]\n'
    expected = ['+STR', '+DOC ---', '+SEQ []', '=VAL :a', '=VAL :b', '=VAL :c', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_CXX2():
    yaml = '--- &anchor a: b\n'
    expected = ['+STR', '+DOC ---', '=VAL &anchor :a']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected
