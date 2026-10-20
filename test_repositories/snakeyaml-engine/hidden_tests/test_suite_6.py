import pytest

from src.snakeyaml_engine import iter_events


def test_case_62EZ():
    yaml = '---\nx: { y: z }in: valid\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :x', '+MAP {}', '=VAL :y', '=VAL :z', '-MAP']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_652Z():
    yaml = '{ ?foo: bar,\nbar: 42\n}\n'
    expected = ['+STR', '+DOC', '+MAP {}', '=VAL :?foo', '=VAL :bar', '=VAL :bar', '=VAL :42', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_65WH():
    yaml = '- foo\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL :foo', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_6BFJ():
    yaml = '---\n&mapping\n&key [ &item a, b, c ]: value\n'
    expected = ['+STR', '+DOC ---', '+MAP &mapping', '+SEQ [] &key', '=VAL &item :a', '=VAL :b', '=VAL :c', '-SEQ', '=VAL :value', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_6CA3():
    yaml = '\t[\n\t]\n'
    expected = ['+STR']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_6CK3():
    yaml = '%TAG !e! tag:example.com,2000:app/\n---\n- !local foo\n- !!str bar\n- !e!tag%21 baz\n'
    expected = ['+STR', '+DOC ---', '+SEQ', '=VAL <!local> :foo', '=VAL <tag:yaml.org,2002:str> :bar', '=VAL <tag:example.com,2000:app/tag!> :baz', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_6FWR():
    yaml = '--- |+\n ab\n \n  \n...\n'
    expected = ['+STR', '+DOC ---', '=VAL |ab\\n\\n \\n', '-DOC ...', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_6H3V():
    yaml = "'foo: bar\\': baz'\n"
    expected = ['+STR', '+DOC', '+MAP', "=VAL 'foo: bar\\\\", "=VAL :baz'", '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_6HB6():
    yaml = '  # Leading comment line spaces are\n   # neither content nor indentation.\n    \nNot indented:\n By one space: |\n    By four\n      spaces\n Flow style: [    # Leading spaces\n   By two,        # in flow style\n  Also by two,    # are neither\n  \tStill by two   # content nor\n    ]             # indentation.\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :Not indented', '+MAP', '=VAL :By one space', '=VAL |By four\\n  spaces\\n', '=VAL :Flow style', '+SEQ []', '=VAL :By two', '=VAL :Also by two', '=VAL :Still by two', '-SEQ', '-MAP', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_6JQW():
    yaml = '# ASCII Art\n--- |\n  \\//||\\/||\n  // ||  ||__\n'
    expected = ['+STR', '+DOC ---', '=VAL |\\\\//||\\\\/||\\n// ||  ||__\\n', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_6JTT():
    yaml = '---\n[ [ a, b, c ]\n'
    expected = ['+STR', '+DOC ---', '+SEQ []', '+SEQ []', '=VAL :a', '=VAL :b', '=VAL :c', '-SEQ']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_6JWB():
    yaml = 'foo: !!seq\n  - !!str a\n  - !!map\n    key: !!str value\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '+SEQ <tag:yaml.org,2002:seq>', '=VAL <tag:yaml.org,2002:str> :a', '+MAP <tag:yaml.org,2002:map>', '=VAL :key', '=VAL <tag:yaml.org,2002:str> :value', '-MAP', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_6LVF():
    yaml = '%FOO  bar baz # Should be ignored\n              # with a warning.\n--- "foo"\n'
    expected = ['+STR', '+DOC ---', '=VAL "foo', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_6M2F():
    yaml = '? &a a\n: &b b\n: *a\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL &a :a', '=VAL &b :b']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_6PBE():
    yaml = '---\n?\n- a\n- b\n:\n- c\n- d\n'
    expected = ['+STR', '+DOC ---', '+MAP', '+SEQ', '=VAL :a', '=VAL :b', '-SEQ', '+SEQ', '=VAL :c', '=VAL :d', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_6S55():
    yaml = 'key:\n - bar\n - baz\n invalid\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key', '+SEQ', '=VAL :bar', '=VAL :baz']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_6SLA():
    yaml = '"foo\\nbar:baz\\tx \\\\$%^&*()x": 23\n\'x\\ny:z\\tx $%^&*()x\': 24\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL "foo\\nbar:baz\\tx \\\\$%^&*()x', '=VAL :23', "=VAL 'x\\\\ny:z\\\\tx $%^&*()x", '=VAL :24', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_6VJK():
    yaml = '>\n Sammy Sosa completed another\n fine season with great stats.\n\n   63 Home Runs\n   0.288 Batting Average\n\n What a year!\n'
    expected = ['+STR', '+DOC', '=VAL >Sammy Sosa completed another fine season with great stats.\\n\\n  63 Home Runs\\n  0.288 Batting Average\\n\\nWhat a year!\\n', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_6WLZ():
    yaml = '# Private\n---\n!foo "bar"\n...\n# Global\n%TAG ! tag:example.com,2000:app/\n---\n!foo "bar"\n'
    expected = ['+STR', '+DOC ---', '=VAL <!foo> "bar', '-DOC ...', '+DOC ---', '=VAL <tag:example.com,2000:app/foo> "bar', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_6WPF():
    yaml = '---\n"\n  foo \n \n    bar\n\n  baz\n"\n'
    expected = ['+STR', '+DOC ---', '=VAL " foo\\nbar\\nbaz ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_6XDY():
    yaml = '---\n---\n'
    expected = ['+STR', '+DOC ---', '=VAL :', '-DOC', '+DOC ---', '=VAL :', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
