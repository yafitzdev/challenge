import pytest

from src.snakeyaml_engine import iter_events


def test_case_J3BT():
    yaml = '# Tabs and spaces\nquoted: "Quoted \t"\nblock:\t|\n  void main() {\n  \tprintf("Hello, world!\\n");\n  }\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :quoted', '=VAL "Quoted \\t', '=VAL :block', '=VAL |void main() {\\n\\tprintf("Hello, world!\\\\n");\\n}\\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_J5UC():
    yaml = 'foo: blue\nbar: arrr\nbaz: jazz\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '=VAL :blue', '=VAL :bar', '=VAL :arrr', '=VAL :baz', '=VAL :jazz', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_J7PZ():
    yaml = '# The !!omap tag is one of the optional types\n# introduced for YAML 1.1. In 1.2, it is not\n# part of the standard tags and should not be\n# enabled by default.\n# Ordered maps are represented as\n# A sequence of mappings, with\n# each mapping having one key\n--- !!omap\n- Mark McGwire: 65\n- Sammy Sosa: 63\n- Ken Griffy: 58\n'
    expected = ['+STR', '+DOC ---', '+SEQ <tag:yaml.org,2002:omap>', '+MAP', '=VAL :Mark McGwire', '=VAL :65', '-MAP', '+MAP', '=VAL :Sammy Sosa', '=VAL :63', '-MAP', '+MAP', '=VAL :Ken Griffy', '=VAL :58', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_J7VC():
    yaml = 'one: 2\n\n\nthree: 4\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :one', '=VAL :2', '=VAL :three', '=VAL :4', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_J9HZ():
    yaml = '---\nhr: # 1998 hr ranking\n  - Mark McGwire\n  - Sammy Sosa\nrbi:\n  # 1998 rbi ranking\n  - Sammy Sosa\n  - Ken Griffey\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :hr', '+SEQ', '=VAL :Mark McGwire', '=VAL :Sammy Sosa', '-SEQ', '=VAL :rbi', '+SEQ', '=VAL :Sammy Sosa', '=VAL :Ken Griffey', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_JEF9_00():
    yaml = '- |+\n\n\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL |\\n\\n', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_JEF9_02():
    yaml = '- |+\n   '
    expected = ['+STR', '+DOC', '+SEQ', '=VAL |', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_JHB9():
    yaml = '# Ranking of 1998 home runs\n---\n- Mark McGwire\n- Sammy Sosa\n- Ken Griffey\n\n# Team ranking\n---\n- Chicago Cubs\n- St Louis Cardinals\n'
    expected = ['+STR', '+DOC ---', '+SEQ', '=VAL :Mark McGwire', '=VAL :Sammy Sosa', '=VAL :Ken Griffey', '-SEQ', '-DOC', '+DOC ---', '+SEQ', '=VAL :Chicago Cubs', '=VAL :St Louis Cardinals', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_JKF3():
    yaml = '- - "bar\nbar": x\n'
    expected = ['+STR', '+DOC', '+SEQ', '+SEQ', '=VAL "bar bar']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_JQ4R():
    yaml = 'block sequence:\n  - one\n  - two : three\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :block sequence', '+SEQ', '=VAL :one', '+MAP', '=VAL :two', '=VAL :three', '-MAP', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_JR7V():
    yaml = '- a?string\n- another ? string\n- key: value?\n- [a?string]\n- [another ? string]\n- {key: value? }\n- {key: value?}\n- {key?: value }\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL :a?string', '=VAL :another ? string', '+MAP', '=VAL :key', '=VAL :value?', '-MAP', '+SEQ []', '=VAL :a?string', '-SEQ', '+SEQ []', '=VAL :another ? string', '-SEQ', '+MAP {}', '=VAL :key', '=VAL :value?', '-MAP', '+MAP {}', '=VAL :key', '=VAL :value?', '-MAP', '+MAP {}', '=VAL :key?', '=VAL :value', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_JS2J():
    yaml = 'First occurrence: &anchor Value\nSecond occurrence: *anchor\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :First occurrence', '=VAL &anchor :Value', '=VAL :Second occurrence', '=ALI *anchor', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_JTV5():
    yaml = '? a\n  true\n: null\n  d\n? e\n  42\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :a true', '=VAL :null d', '=VAL :e 42', '=VAL :', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_JY7Z():
    yaml = 'key1: "quoted1"\nkey2: "quoted2" no key: nor value\nkey3: "quoted3"\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key1', '=VAL "quoted1', '=VAL :key2', '=VAL "quoted2']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected
