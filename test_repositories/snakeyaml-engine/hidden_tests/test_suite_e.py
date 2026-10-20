import pytest

from src.snakeyaml_engine import iter_events


def test_case_E76Z():
    yaml = '&a a: &b b\n*b : *a\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL &a :a', '=VAL &b :b', '=ALI *b', '=ALI *a', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_EB22():
    yaml = '---\nscalar1 # comment\n%YAML 1.2\n---\nscalar2\n'
    expected = ['+STR', '+DOC ---', '=VAL :scalar1']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_EHF6():
    yaml = '!!map {\n  k: !!seq\n  [ a, !!str b]\n}\n'
    expected = ['+STR', '+DOC', '+MAP {} <tag:yaml.org,2002:map>', '=VAL :k', '+SEQ [] <tag:yaml.org,2002:seq>', '=VAL :a', '=VAL <tag:yaml.org,2002:str> :b', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_EX5H():
    yaml = '---\na\nb  \n  c\nd\n\ne\n'
    expected = ['+STR', '+DOC ---', '=VAL :a b c d\\ne', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_EXG3():
    yaml = '---\n---word1\nword2\n'
    expected = ['+STR', '+DOC ---', '=VAL :---word1 word2', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
