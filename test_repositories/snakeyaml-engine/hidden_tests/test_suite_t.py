import pytest

from src.snakeyaml_engine import iter_events


def test_case_T26H():
    yaml = '--- |\n \n  \n  literal\n   \n  \n  text\n\n # Comment\n'
    expected = ['+STR', '+DOC ---', '=VAL |\\n\\nliteral\\n \\n\\ntext\\n', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_T4YY():
    yaml = "---\n' 1st non-empty\n\n 2nd non-empty \n 3rd non-empty '\n"
    expected = ['+STR', '+DOC ---', "=VAL ' 1st non-empty\\n2nd non-empty 3rd non-empty ", '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_T5N4():
    yaml = '--- |\n literal\n \ttext\n\n\n'
    expected = ['+STR', '+DOC ---', '=VAL |literal\\n\\ttext\\n', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_T833():
    yaml = '---\n{\n foo: 1\n bar: 2 }\n'
    expected = ['+STR', '+DOC ---', '+MAP {}', '=VAL :foo', '=VAL :1 bar']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_TD5N():
    yaml = '- item1\n- item2\ninvalid\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL :item1', '=VAL :item2']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_TE2A():
    yaml = 'block mapping:\n key: value\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :block mapping', '+MAP', '=VAL :key', '=VAL :value', '-MAP', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_TL85():
    yaml = '"\n  foo \n \n  \t bar\n\n  baz\n"\n'
    expected = ['+STR', '+DOC', '=VAL " foo\\nbar\\nbaz ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
