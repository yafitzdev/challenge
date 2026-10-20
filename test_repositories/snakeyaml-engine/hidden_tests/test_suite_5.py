import pytest

from src.snakeyaml_engine import iter_events


def test_case_52DL():
    yaml = '---\n! a\n'
    expected = ['+STR', '+DOC ---', '=VAL <!> :a', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_55WF():
    yaml = '---\n"\\."\n'
    expected = ['+STR', '+DOC ---']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_565N():
    yaml = 'canonical: !!binary "\\\n R0lGODlhDAAMAIQAAP//9/X17unp5WZmZgAAAOfn515eXvPz7Y6OjuDg4J+fn5\\\n OTk6enp56enmlpaWNjY6Ojo4SEhP/++f/++f/++f/++f/++f/++f/++f/++f/+\\\n +f/++f/++f/++f/++f/++SH+Dk1hZGUgd2l0aCBHSU1QACwAAAAADAAMAAAFLC\\\n AgjoEwnuNAFOhpEMTRiggcz4BNJHrv/zCFcLiwMWYNG84BwwEeECcgggoBADs="\ngeneric: !!binary |\n R0lGODlhDAAMAIQAAP//9/X17unp5WZmZgAAAOfn515eXvPz7Y6OjuDg4J+fn5\n OTk6enp56enmlpaWNjY6Ojo4SEhP/++f/++f/++f/++f/++f/++f/++f/++f/+\n +f/++f/++f/++f/++f/++SH+Dk1hZGUgd2l0aCBHSU1QACwAAAAADAAMAAAFLC\n AgjoEwnuNAFOhpEMTRiggcz4BNJHrv/zCFcLiwMWYNG84BwwEeECcgggoBADs=\ndescription:\n The binary value above is a tiny arrow encoded as a gif image.\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :canonical', '=VAL <tag:yaml.org,2002:binary> "R0lGODlhDAAMAIQAAP//9/X17unp5WZmZgAAAOfn515eXvPz7Y6OjuDg4J+fn5OTk6enp56enmlpaWNjY6Ojo4SEhP/++f/++f/++f/++f/++f/++f/++f/++f/++f/++f/++f/++f/++f/++SH+Dk1hZGUgd2l0aCBHSU1QACwAAAAADAAMAAAFLCAgjoEwnuNAFOhpEMTRiggcz4BNJHrv/zCFcLiwMWYNG84BwwEeECcgggoBADs=', '=VAL :generic', '=VAL <tag:yaml.org,2002:binary> |R0lGODlhDAAMAIQAAP//9/X17unp5WZmZgAAAOfn515eXvPz7Y6OjuDg4J+fn5\\nOTk6enp56enmlpaWNjY6Ojo4SEhP/++f/++f/++f/++f/++f/++f/++f/++f/+\\n+f/++f/++f/++f/++f/++SH+Dk1hZGUgd2l0aCBHSU1QACwAAAAADAAMAAAFLC\\nAgjoEwnuNAFOhpEMTRiggcz4BNJHrv/zCFcLiwMWYNG84BwwEeECcgggoBADs=\\n', '=VAL :description', '=VAL :The binary value above is a tiny arrow encoded as a gif image.', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_57H4():
    yaml = 'sequence: !!seq\n- entry\n- !!seq\n - nested\nmapping: !!map\n foo: bar\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :sequence', '+SEQ <tag:yaml.org,2002:seq>', '=VAL :entry', '+SEQ <tag:yaml.org,2002:seq>', '=VAL :nested', '-SEQ', '-SEQ', '=VAL :mapping', '+MAP <tag:yaml.org,2002:map>', '=VAL :foo', '=VAL :bar', '-MAP', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_58MP():
    yaml = '{x: :x}\n'
    expected = ['+STR', '+DOC', '+MAP {}', '=VAL :x']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_5BVJ():
    yaml = 'literal: |\n  some\n  text\nfolded: >\n  some\n  text\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :literal', '=VAL |some\\ntext\\n', '=VAL :folded', '=VAL >some text\\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_5C5M():
    yaml = '- { one : two , three: four , }\n- {five: six,seven : eight}\n'
    expected = ['+STR', '+DOC', '+SEQ', '+MAP {}', '=VAL :one', '=VAL :two', '=VAL :three', '=VAL :four', '-MAP', '+MAP {}', '=VAL :five', '=VAL :six', '=VAL :seven', '=VAL :eight', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_5GBF():
    yaml = 'Folding:\n  "Empty line\n   \t\n  as a line feed"\nChomping: |\n  Clipped empty lines\n \n\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :Folding', '=VAL "Empty line\\nas a line feed', '=VAL :Chomping', '=VAL |Clipped empty lines\\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_5KJE():
    yaml = '- [ one, two, ]\n- [three ,four]\n'
    expected = ['+STR', '+DOC', '+SEQ', '+SEQ []', '=VAL :one', '=VAL :two', '-SEQ', '+SEQ []', '=VAL :three', '=VAL :four', '-SEQ', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_5LLU():
    yaml = 'block scalar: >\n \n  \n   \n invalid\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :block scalar']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_5NYZ():
    yaml = 'key:    # Comment\n  value\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key', '=VAL :value', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_5T43():
    yaml = '- { "key":value }\n- { "key"::value }\n'
    expected = ['+STR', '+DOC', '+SEQ', '+MAP {}', '=VAL "key', '=VAL :value', '-MAP', '+MAP {}', '=VAL "key']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_5TRB():
    yaml = '---\n"\n---\n"\n'
    expected = ['+STR', '+DOC ---']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_5TYM():
    yaml = '%TAG !m! !my-\n--- # Bulb here\n!m!light fluorescent\n...\n%TAG !m! !my-\n--- # Color here\n!m!light green\n'
    expected = ['+STR', '+DOC ---', '=VAL <!my-light> :fluorescent', '-DOC ...', '+DOC ---', '=VAL <!my-light> :green', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_5U3A():
    yaml = 'key: - a\n     - b\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_5WE3():
    yaml = '? explicit key # Empty value\n? |\n  block key\n: - one # Explicit compact\n  - two # block value\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :explicit key', '=VAL :', '=VAL |block key\\n', '+SEQ', '=VAL :one', '=VAL :two', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
