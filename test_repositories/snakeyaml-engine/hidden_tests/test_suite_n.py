import pytest

from src.snakeyaml_engine import iter_events


def test_case_N4JP():
    yaml = 'map:\n  key1: "quoted1"\n key2: "bad indentation"\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :map', '+MAP', '=VAL :key1', '=VAL "quoted1', '-MAP']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_N782():
    yaml = '[\n--- ,\n...\n]\n'
    expected = ['+STR', '+DOC', '+SEQ []']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_NAT4():
    yaml = '---\na: \'\n  \'\nb: \'  \n  \'\nc: "\n  "\nd: "  \n  "\ne: \'\n\n  \'\nf: "\n\n  "\ng: \'\n\n\n  \'\nh: "\n\n\n  "\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :a', "=VAL ' ", '=VAL :b', "=VAL ' ", '=VAL :c', '=VAL " ', '=VAL :d', '=VAL " ', '=VAL :e', "=VAL '\\n", '=VAL :f', '=VAL "\\n', '=VAL :g', "=VAL '\\n\\n", '=VAL :h', '=VAL "\\n\\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_NB6Z():
    yaml = 'key:\n  value\n  with\n  \t\n  tabs\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key', '=VAL :value with']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_NHX8():
    yaml = ':\n\n\n'
    expected = ['+STR', '+DOC', '+MAP']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_NJ66():
    yaml = '---\n- { single line: value}\n- { multi\n  line: value}\n'
    expected = ['+STR', '+DOC ---', '+SEQ', '+MAP {}', '=VAL :single line', '=VAL :value', '-MAP', '+MAP {}', '=VAL :multi line', '=VAL :']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_NKF9():
    yaml = '---\nkey: value\n: empty key\n---\n{\n key: value, : empty key\n}\n---\n# empty key and value\n:\n---\n# empty key and value\n{ : }\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :key', '=VAL :value']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_NP9H():
    yaml = '"folded \nto a space,\t\n \nto a line feed, or \t\\\n \\ \tnon-content"\n'
    expected = ['+STR', '+DOC', '=VAL "folded to a space,\\nto a line feed, or \\t \\tnon-content', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
