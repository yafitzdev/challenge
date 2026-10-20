import pytest

from src.snakeyaml_engine import iter_events


def test_case_R4YG():
    yaml = '- |\n detected\n- >\n \n  \n  # detected\n- |1\n  explicit\n- >\n \t\n detected\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL |detected\\n', '=VAL >\\n\\n# detected\\n', '=VAL | explicit\\n', '=VAL >\\t\\ndetected\\n', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_R52L():
    yaml = '---\n{ top1: [item1, {key2: value2}, item3], top2: value2 }\n'
    expected = ['+STR', '+DOC ---', '+MAP {}', '=VAL :top1', '+SEQ []', '=VAL :item1', '+MAP {}', '=VAL :key2', '=VAL :value2', '-MAP', '=VAL :item3', '-SEQ', '=VAL :top2', '=VAL :value2', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_RHX7():
    yaml = '---\nkey: value\n%YAML 1.2\n---\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :key', '=VAL :value', '-MAP']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_RLU9():
    yaml = 'foo:\n- 42\nbar:\n  - 44\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '+SEQ', '=VAL :42', '-SEQ', '=VAL :bar', '+SEQ', '=VAL :44', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_RTP8():
    yaml = '%YAML 1.2\n---\nDocument\n... # Suffix\n'
    expected = ['+STR', '+DOC ---', '=VAL :Document', '-DOC ...', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_RXY3():
    yaml = "---\n'\n...\n'\n"
    expected = ['+STR', '+DOC ---']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_RZP5():
    yaml = 'a: "double\n  quotes" # lala\nb: plain\n value  # lala\nc  : #lala\n  d\n? # lala\n - seq1\n: # lala\n - #lala\n  seq2\ne: &node # lala\n - x: y\nblock: > # lala\n  abcde\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :a', '=VAL "double quotes', '=VAL :b', '=VAL :plain value', '=VAL :c', '=VAL :d', '+SEQ', '=VAL :seq1', '-SEQ', '+SEQ', '=VAL :seq2', '-SEQ', '=VAL :e', '+SEQ &node', '+MAP', '=VAL :x', '=VAL :y', '-MAP', '-SEQ', '=VAL :block', '=VAL >abcde\\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_RZT7():
    yaml = '---\nTime: 2001-11-23 15:01:42 -5\nUser: ed\nWarning:\n  This is an error message\n  for the log file\n---\nTime: 2001-11-23 15:02:31 -5\nUser: ed\nWarning:\n  A slightly different error\n  message.\n---\nDate: 2001-11-23 15:03:17 -5\nUser: ed\nFatal:\n  Unknown variable "bar"\nStack:\n  - file: TopClass.py\n    line: 23\n    code: |\n      x = MoreObject("345\\n")\n  - file: MoreClass.py\n    line: 58\n    code: |-\n      foo = bar\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :Time', '=VAL :2001-11-23 15:01:42 -5', '=VAL :User', '=VAL :ed', '=VAL :Warning', '=VAL :This is an error message for the log file', '-MAP', '-DOC', '+DOC ---', '+MAP', '=VAL :Time', '=VAL :2001-11-23 15:02:31 -5', '=VAL :User', '=VAL :ed', '=VAL :Warning', '=VAL :A slightly different error message.', '-MAP', '-DOC', '+DOC ---', '+MAP', '=VAL :Date', '=VAL :2001-11-23 15:03:17 -5', '=VAL :User', '=VAL :ed', '=VAL :Fatal', '=VAL :Unknown variable "bar"', '=VAL :Stack', '+SEQ', '+MAP', '=VAL :file', '=VAL :TopClass.py', '=VAL :line', '=VAL :23', '=VAL :code', '=VAL |x = MoreObject("345\\\\n")\\n', '-MAP', '+MAP', '=VAL :file', '=VAL :MoreClass.py', '=VAL :line', '=VAL :58', '=VAL :code', '=VAL |foo = bar', '-MAP', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
