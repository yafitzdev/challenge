import pytest

from src.snakeyaml_engine import iter_events


def test_case_G4RS():
    yaml = 'unicode: "Sosa did fine.\\u263A"\ncontrol: "\\b1998\\t1999\\t2000\\n"\nhex esc: "\\x0d\\x0a is \\r\\n"\n\nsingle: \'"Howdy!" he cried.\'\nquoted: \' # Not a \'\'comment\'\'.\'\ntie-fighter: \'|\\-*-/|\'\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :unicode', '=VAL "Sosa did fine.☺', '=VAL :control', '=VAL "\\b1998\\t1999\\t2000\\n', '=VAL :hex esc', '=VAL "\\r\\n is \\r\\n', '=VAL :single', '=VAL \'"Howdy!" he cried.', '=VAL :quoted', "=VAL ' # Not a 'comment'.", '=VAL :tie-fighter', "=VAL '|\\\\-*-/|", '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_G5U8():
    yaml = '---\n- [-, -]\n'
    expected = ['+STR', '+DOC ---', '+SEQ']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_G7JE():
    yaml = 'a\\nb: 1\nc\n d: 1\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :a\\\\nb', '=VAL :1']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_G992():
    yaml = '>\n folded\n text\n\n\n'
    expected = ['+STR', '+DOC', '=VAL >folded text\\n', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_G9HC():
    yaml = '---\nseq:\n&anchor\n- a\n- b\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :seq']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_GDY7():
    yaml = 'key: value\nthis is #not a: key\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key', '=VAL :value']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_GT5M():
    yaml = '- item1\n&node\n- item2\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL :item1']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected
