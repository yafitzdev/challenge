import pytest

from src.snakeyaml_engine import iter_events


def test_case_Q4CL():
    yaml = 'key1: "quoted1"\nkey2: "quoted2" trailing content\nkey3: "quoted3"\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key1', '=VAL "quoted1', '=VAL :key2', '=VAL "quoted2']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_Q5MG():
    yaml = '\t{}\n'
    expected = ['+STR']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_Q88A():
    yaml = '- [ a, b ]\n- { a: b }\n- "a"\n- \'b\'\n- c\n'
    expected = ['+STR', '+DOC', '+SEQ', '+SEQ []', '=VAL :a', '=VAL :b', '-SEQ', '+MAP {}', '=VAL :a', '=VAL :b', '-MAP', '=VAL "a', "=VAL 'b", '=VAL :c', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_Q9WF():
    yaml = '{ first: Sammy, last: Sosa }:\n# Statistics:\n  hr:  # Home runs\n     65\n  avg: # Average\n   0.278\n'
    expected = ['+STR', '+DOC', '+MAP', '+MAP {}', '=VAL :first', '=VAL :Sammy', '=VAL :last', '=VAL :Sosa', '-MAP', '+MAP', '=VAL :hr', '=VAL :65', '=VAL :avg', '=VAL :0.278', '-MAP', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_QB6E():
    yaml = '---\nquoted: "a\nb\nc"\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :quoted', '=VAL "a b c', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_QF4Y():
    yaml = '[\nfoo: bar\n]\n'
    expected = ['+STR', '+DOC', '+SEQ []', '+MAP {}', '=VAL :foo', '=VAL :bar', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_QLJ7():
    yaml = '%TAG !prefix! tag:example.com,2011:\n--- !prefix!A\na: b\n--- !prefix!B\nc: d\n--- !prefix!C\ne: f\n'
    expected = ['+STR', '+DOC ---', '+MAP <tag:example.com,2011:A>', '=VAL :a', '=VAL :b', '-MAP', '-DOC', '+DOC ---']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_QT73():
    yaml = '# comment\n...\n'
    expected = ['+STR', '+DOC']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected
