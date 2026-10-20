import pytest

from src.snakeyaml_engine import iter_events


def test_case_D83L():
    yaml = '- |2-\n  explicit indent and chomp\n- |-2\n  chomp and explicit indent\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL |explicit indent and chomp', '=VAL |chomp and explicit indent', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_D88J():
    yaml = 'a: [b, c]\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :a', '+SEQ []', '=VAL :b', '=VAL :c', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_D9TU():
    yaml = 'foo: bar\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '=VAL :bar', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_DBG4():
    yaml = '# Outside flow collection:\n- ::vector\n- ": - ()"\n- Up, up, and away!\n- -123\n- http://example.com/foo#bar\n# Inside flow collection:\n- [ ::vector,\n  ": - ()",\n  "Up, up and away!",\n  -123,\n  http://example.com/foo#bar ]\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL :::vector', '=VAL ": - ()', '=VAL :Up, up, and away!', '=VAL :-123', '=VAL :http://example.com/foo#bar', '+SEQ []']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_DC7X():
    yaml = 'a: b\t\nseq:\t\n - a\t\nc: d\t#X\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :a', '=VAL :b', '=VAL :seq', '+SEQ', '=VAL :a', '-SEQ', '=VAL :c', '=VAL :d', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_DE56_00():
    yaml = '"1 trailing\\t\n    tab"\n'
    expected = ['+STR', '+DOC', '=VAL "1 trailing\\t tab', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_DE56_01():
    yaml = '"2 trailing\\t  \n    tab"\n'
    expected = ['+STR', '+DOC', '=VAL "2 trailing\\t tab', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_DE56_02():
    yaml = '"3 trailing\\\t\n    tab"\n'
    expected = ['+STR', '+DOC', '=VAL "3 trailing\\t tab', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_DE56_03():
    yaml = '"4 trailing\\\t  \n    tab"\n'
    expected = ['+STR', '+DOC', '=VAL "4 trailing\\t tab', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_DE56_05():
    yaml = '"6 trailing\t  \n    tab"\n'
    expected = ['+STR', '+DOC', '=VAL "6 trailing tab', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_DFF7():
    yaml = '{\n? explicit: entry,\nimplicit: entry,\n?\n}\n'
    expected = ['+STR', '+DOC', '+MAP {}', '=VAL :explicit', '=VAL :entry', '=VAL :implicit', '=VAL :entry', '=VAL :', '=VAL :', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_DHP8():
    yaml = '[foo, bar, 42]\n'
    expected = ['+STR', '+DOC', '+SEQ []', '=VAL :foo', '=VAL :bar', '=VAL :42', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_DK3J():
    yaml = '--- >\nline1\n# no comment\nline3\n'
    expected = ['+STR', '+DOC ---', '=VAL >', '-DOC']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_DK4H():
    yaml = '---\n[ key\n  : value ]\n'
    expected = ['+STR', '+DOC ---', '+SEQ []', '=VAL :key']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_DK95_00():
    yaml = 'foo:\n \tbar\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '=VAL :bar', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_DK95_01():
    yaml = 'foo: "bar\n\tbaz"\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '=VAL "bar baz', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_DK95_02():
    yaml = 'foo: "bar\n  \tbaz"\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '=VAL "bar baz', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_DK95_03():
    yaml = ' \t\nfoo: 1\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '=VAL :1', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_DK95_05():
    yaml = 'foo: 1\n \t\nbar: 2\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '=VAL :1', '=VAL :bar', '=VAL :2', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_DK95_06():
    yaml = 'foo:\n  a: 1\n  \tb: 2\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '+MAP', '=VAL :a', '=VAL :1']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_DK95_07():
    yaml = '%YAML 1.2\n\t\n---\n'
    expected = ['+STR', '+DOC ---', '=VAL :', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_DK95_08():
    yaml = 'foo: "bar\n \t \t baz \t \t "\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '=VAL "bar baz \\t \\t ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_DMG6():
    yaml = 'key:\n  ok: 1\n wrong: 2\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key', '+MAP', '=VAL :ok', '=VAL :1', '-MAP']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_DWX9():
    yaml = '|\n \n  \n  literal\n   \n  \n  text\n\n # Comment\n'
    expected = ['+STR', '+DOC', '=VAL |\\n\\nliteral\\n \\n\\ntext\\n', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
