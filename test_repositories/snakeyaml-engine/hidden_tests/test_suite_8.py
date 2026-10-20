import pytest

from src.snakeyaml_engine import iter_events


def test_case_82AN():
    yaml = '---word1\nword2\n'
    expected = ['+STR', '+DOC', '=VAL :---word1 word2', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_87E4():
    yaml = "'implicit block key' : [\n  'implicit flow key' : value,\n ]\n"
    expected = ['+STR', '+DOC', '+MAP', "=VAL 'implicit block key", '+SEQ []', '+MAP {}', "=VAL 'implicit flow key", '=VAL :value', '-MAP', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_8CWC():
    yaml = '---\nkey ends with two colons::: value\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :key ends with two colons::', '=VAL :value', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_8G76():
    yaml = '  # Comment\n   \n\n\n'
    expected = ['+STR', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_8KB6():
    yaml = '---\n- { single line, a: b}\n- { multi\n  line, a: b}\n'
    expected = ['+STR', '+DOC ---', '+SEQ', '+MAP {}', '=VAL :single line', '=VAL :', '=VAL :a', '=VAL :b', '-MAP', '+MAP {}', '=VAL :multi line', '=VAL :', '=VAL :a', '=VAL :b', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_8QBE():
    yaml = 'key:\n - item1\n - item2\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key', '+SEQ', '=VAL :item1', '=VAL :item2', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_8UDB():
    yaml = '[\n"double\n quoted", \'single\n           quoted\',\nplain\n text, [ nested ],\nsingle: pair,\n]\n'
    expected = ['+STR', '+DOC', '+SEQ []', '=VAL "double quoted', "=VAL 'single quoted", '=VAL :plain text', '+SEQ []', '=VAL :nested', '-SEQ', '+MAP {}', '=VAL :single', '=VAL :pair', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_8XDJ():
    yaml = 'key: word1\n#  xxx\n  word2\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key', '=VAL :word1']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_8XYN():
    yaml = '---\n- &😁 unicode anchor\n'
    expected = ['+STR', '+DOC ---', '+SEQ', '=VAL &😁 :unicode anchor', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
