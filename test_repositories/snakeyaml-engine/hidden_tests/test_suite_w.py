import pytest

from src.snakeyaml_engine import iter_events


def test_case_W42U():
    yaml = '- # Empty\n- |\n block node\n- - one # Compact\n  - two # sequence\n- one: two # Compact mapping\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL :', '=VAL |block node\\n', '+SEQ', '=VAL :one', '=VAL :two', '-SEQ', '+MAP', '=VAL :one', '=VAL :two', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_W4TN():
    yaml = '%YAML 1.2\n--- |\n%!PS-Adobe-2.0\n...\n%YAML 1.2\n---\n# Empty\n...\n'
    expected = ['+STR', '+DOC ---', '=VAL |']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_W9L4():
    yaml = '---\nblock scalar: |\n     \n  more spaces at the beginning\n  are invalid\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :block scalar']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_WZ62():
    yaml = '{\n  foo : !!str,\n  !!str : bar,\n}\n'
    expected = ['+STR', '+DOC', '+MAP {}', '=VAL :foo']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected
