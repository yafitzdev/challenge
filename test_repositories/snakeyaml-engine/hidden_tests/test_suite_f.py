import pytest

from src.snakeyaml_engine import iter_events


def test_case_F2C7():
    yaml = ' - &a !!str a\n - !!int 2\n - !!int &c 4\n - &d d\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL &a <tag:yaml.org,2002:str> :a', '=VAL <tag:yaml.org,2002:int> :2', '=VAL &c <tag:yaml.org,2002:int> :4', '=VAL &d :d', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_F3CP():
    yaml = '---\n{ a: [b, c, { d: [e, f] } ] }\n'
    expected = ['+STR', '+DOC ---', '+MAP {}', '=VAL :a', '+SEQ []', '=VAL :b', '=VAL :c', '+MAP {}', '=VAL :d', '+SEQ []', '=VAL :e', '=VAL :f', '-SEQ', '-MAP', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_F6MC():
    yaml = '---\na: >2\n   more indented\n  regular\nb: >2\n\n\n   more indented\n  regular\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :a', '=VAL > more indented\\nregular\\n', '=VAL :b', '=VAL >\\n\\n more indented\\nregular\\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_F8F9():
    yaml = ' # Strip\n  # Comments:\nstrip: |-\n  # text\n  \n # Clip\n  # comments:\n\nclip: |\n  # text\n \n # Keep\n  # comments:\n\nkeep: |+\n  # text\n\n # Trail\n  # comments.\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :strip', '=VAL |# text', '=VAL :clip', '=VAL |# text\\n', '=VAL :keep', '=VAL |# text\\n\\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_FBC9():
    yaml = 'safe: a!"#$%&\'()*+,-./09:;<=>?@AZ[\\]^_`az{|}~\n     !"#$%&\'()*+,-./09:;<=>?@AZ[\\]^_`az{|}~\nsafe question mark: ?foo\nsafe colon: :foo\nsafe dash: -foo\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :safe', '=VAL :a!"#$%&\'()*+,-./09:;<=>?@AZ[\\\\]^_`az{|}~ !"#$%&\'()*+,-./09:;<=>?@AZ[\\\\]^_`az{|}~', '=VAL :safe question mark', '=VAL :?foo', '=VAL :safe colon', '=VAL ::foo', '=VAL :safe dash', '=VAL :-foo', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_FH7J():
    yaml = '- !!str\n-\n  !!null : a\n  b: !!str\n- !!str : !!null\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL <tag:yaml.org,2002:str> :', '+MAP', '=VAL <tag:yaml.org,2002:null> :', '=VAL :a', '=VAL :b', '=VAL <tag:yaml.org,2002:str> :', '-MAP', '+MAP', '=VAL <tag:yaml.org,2002:str> :', '=VAL <tag:yaml.org,2002:null> :', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_FP8R():
    yaml = '--- >\nline1\nline2\nline3\n'
    expected = ['+STR', '+DOC ---', '=VAL >', '-DOC']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_FRK4():
    yaml = '{\n  ? foo :,\n  : bar,\n}\n'
    expected = ['+STR', '+DOC', '+MAP {}', '=VAL :foo', '=VAL :']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_FTA2():
    yaml = '--- &sequence\n- a\n'
    expected = ['+STR', '+DOC ---', '+SEQ &sequence', '=VAL :a', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_FUP4():
    yaml = '[a, [b, c]]\n'
    expected = ['+STR', '+DOC', '+SEQ []', '=VAL :a', '+SEQ []', '=VAL :b', '=VAL :c', '-SEQ', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
