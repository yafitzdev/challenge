import pytest

from src.snakeyaml_engine import iter_events


def test_case_M29M():
    yaml = 'a: |\n ab\n \n cd\n ef\n \n\n...\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :a', '=VAL |ab\\n\\ncd\\nef\\n', '-MAP', '-DOC ...', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_M2N8_00():
    yaml = '- ? : x\n'
    expected = ['+STR', '+DOC', '+SEQ', '+MAP', '+MAP']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_M2N8_01():
    yaml = '? []: x\n'
    expected = ['+STR', '+DOC', '+MAP', '+MAP', '+SEQ []', '-SEQ', '=VAL :x', '-MAP', '=VAL :', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_M5C3():
    yaml = 'literal: |2\n  value\nfolded:\n   !foo\n  >1\n value\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :literal', '=VAL |value\\n', '=VAL :folded', '=VAL <!foo> >value\\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_M5DY():
    yaml = '? - Detroit Tigers\n  - Chicago cubs\n:\n  - 2001-07-23\n\n? [ New York Yankees,\n    Atlanta Braves ]\n: [ 2001-07-02, 2001-08-12,\n    2001-08-14 ]\n'
    expected = ['+STR', '+DOC', '+MAP', '+SEQ', '=VAL :Detroit Tigers', '=VAL :Chicago cubs', '-SEQ', '+SEQ', '=VAL :2001-07-23', '-SEQ', '+SEQ []', '=VAL :New York Yankees', '=VAL :Atlanta Braves', '-SEQ', '+SEQ []', '=VAL :2001-07-02', '=VAL :2001-08-12', '=VAL :2001-08-14', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_M6YH():
    yaml = '- |\n x\n-\n foo: bar\n-\n - 42\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL |x\\n', '+MAP', '=VAL :foo', '=VAL :bar', '-MAP', '+SEQ', '=VAL :42', '-SEQ', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_M7A3():
    yaml = 'Bare\ndocument\n...\n# No document\n...\n|\n%!PS-Adobe-2.0 # Not the first line\n'
    expected = ['+STR', '+DOC', '=VAL :Bare document', '-DOC ...']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_M7NX():
    yaml = '---\n{\n a: [\n  b, c, {\n   d: [e, f]\n  }\n ]\n}\n'
    expected = ['+STR', '+DOC ---', '+MAP {}', '=VAL :a', '+SEQ []', '=VAL :b', '=VAL :c', '+MAP {}', '=VAL :d', '+SEQ []', '=VAL :e', '=VAL :f', '-SEQ', '-MAP', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_M9B4():
    yaml = '|\n literal\n \ttext\n\n\n'
    expected = ['+STR', '+DOC', '=VAL |literal\\n\\ttext\\n', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_MUS6_00():
    yaml = '%YAML 1.1#...\n---\n'
    expected = ['+STR']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_MUS6_01():
    yaml = '%YAML 1.2\n---\n%YAML 1.2\n---\n'
    expected = ['+STR', '+DOC ---', '=VAL :']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_MUS6_02():
    yaml = '%YAML  1.1\n---\n'
    expected = ['+STR', '+DOC ---', '=VAL :', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_MUS6_03():
    yaml = '%YAML \t 1.1\n---\n'
    expected = ['+STR', '+DOC ---', '=VAL :', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_MUS6_04():
    yaml = '%YAML 1.1  # comment\n---\n'
    expected = ['+STR', '+DOC ---', '=VAL :', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_MUS6_05():
    yaml = '%YAM 1.1\n---\n'
    expected = ['+STR', '+DOC ---', '=VAL :', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_MUS6_06():
    yaml = '%YAMLL 1.1\n---\n'
    expected = ['+STR', '+DOC ---', '=VAL :', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_MXS3():
    yaml = '- {a: b}\n'
    expected = ['+STR', '+DOC', '+SEQ', '+MAP {}', '=VAL :a', '=VAL :b', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_MYW6():
    yaml = '|-\n ab\n \n \n...\n'
    expected = ['+STR', '+DOC', '=VAL |ab', '-DOC ...', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
