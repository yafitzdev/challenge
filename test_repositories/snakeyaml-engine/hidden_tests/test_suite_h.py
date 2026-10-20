import pytest

from src.snakeyaml_engine import iter_events


def test_case_H2RW():
    yaml = 'foo: 1\n\nbar: 2\n    \ntext: |\n  a\n    \n  b\n\n  c\n \n  d\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '=VAL :1', '=VAL :bar', '=VAL :2', '=VAL :text', '=VAL |a\\n  \\nb\\n\\nc\\n\\nd\\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_H3Z8():
    yaml = '---\nwanted: love ♥ and peace ☮\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :wanted', '=VAL :love ♥ and peace ☮', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_H7J7():
    yaml = 'key: &x\n!!map\n  a: b\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_H7TQ():
    yaml = '%YAML 1.2 foo\n---\n'
    expected = ['+STR']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_HM87_00():
    yaml = '[:x]\n'
    expected = ['+STR', '+DOC', '+SEQ []']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_HM87_01():
    yaml = '[?x]\n'
    expected = ['+STR', '+DOC', '+SEQ []', '=VAL :?x', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_HMK4():
    yaml = 'name: Mark McGwire\naccomplishment: >\n  Mark set a major league\n  home run record in 1998.\nstats: |\n  65 Home Runs\n  0.278 Batting Average\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :name', '=VAL :Mark McGwire', '=VAL :accomplishment', '=VAL >Mark set a major league home run record in 1998.\\n', '=VAL :stats', '=VAL |65 Home Runs\\n0.278 Batting Average\\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_HMQ5():
    yaml = '!!str &a1 "foo":\n  !!str bar\n&a2 baz : *a1\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL &a1 <tag:yaml.org,2002:str> "foo', '=VAL <tag:yaml.org,2002:str> :bar', '=VAL &a2 :baz', '=ALI *a1', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_HS5T():
    yaml = '1st non-empty\n\n 2nd non-empty \n\t3rd non-empty\n'
    expected = ['+STR', '+DOC', '=VAL :1st non-empty\\n2nd non-empty']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_HU3P():
    yaml = 'key:\n  word1 word2\n  no: key\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key', '=VAL :word1 word2 no']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_HWV9():
    yaml = '...\n'
    expected = ['+STR', '+DOC']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected
