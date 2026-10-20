import pytest

from src.snakeyaml_engine import iter_events


def test_case_4ABK():
    yaml = '{\nunquoted : "separate",\nhttp://foo.com,\nomitted value:,\n}\n'
    expected = ['+STR', '+DOC', '+MAP {}', '=VAL :unquoted', '=VAL "separate', '=VAL :http://foo.com', '=VAL :', '=VAL :omitted value', '=VAL :', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_4CQQ():
    yaml = 'plain:\n  This unquoted scalar\n  spans many lines.\n\nquoted: "So does this\n  quoted scalar.\\n"\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :plain', '=VAL :This unquoted scalar spans many lines.', '=VAL :quoted', '=VAL "So does this quoted scalar.\\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_4EJS():
    yaml = '---\na:\n\tb:\n\t\tc: value\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :a']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_4FJ6():
    yaml = '---\n[\n  [ a, [ [[b,c]]: d, e]]: 23\n]\n'
    expected = ['+STR', '+DOC ---', '+SEQ []', '+MAP {}', '+SEQ []', '=VAL :a', '+SEQ []', '+MAP {}', '+SEQ []', '+SEQ []', '=VAL :b', '=VAL :c', '-SEQ', '-SEQ', '=VAL :d', '-MAP', '=VAL :e', '-SEQ', '-SEQ', '=VAL :23', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_4GC6():
    yaml = '\'here\'\'s to "quotes"\'\n'
    expected = ['+STR', '+DOC', '=VAL \'here\'s to "quotes"', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_4H7K():
    yaml = '---\n[ a, b, c ] ]\n'
    expected = ['+STR', '+DOC ---', '+SEQ []', '=VAL :a', '=VAL :b', '=VAL :c', '-SEQ', '-DOC']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_4HVU():
    yaml = 'key:\n   - ok\n   - also ok\n  - wrong\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key', '+SEQ', '=VAL :ok', '=VAL :also ok', '-SEQ']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_4JVG():
    yaml = 'top1: &node1\n  &k1 key1: val1\ntop2: &node2\n  &v2 val2\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :top1', '+MAP &node1', '=VAL &k1 :key1', '=VAL :val1', '-MAP', '=VAL :top2', '=VAL &node2 :']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_4MUZ_00():
    yaml = '{"foo"\n: "bar"}\n'
    expected = ['+STR', '+DOC', '+MAP {}', '=VAL "foo', '=VAL :']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_4MUZ_02():
    yaml = '{foo\n: bar}\n'
    expected = ['+STR', '+DOC', '+MAP {}', '=VAL :foo', '=VAL :']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_4Q9F():
    yaml = '--- >\n ab\n cd\n \n ef\n\n\n gh\n'
    expected = ['+STR', '+DOC ---', '=VAL >ab cd\\nef\\n\\ngh\\n', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_4QFQ():
    yaml = '- |\n detected\n- >\n \n  \n  # detected\n- |1\n  explicit\n- >\n detected\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL |detected\\n', '=VAL >\\n\\n# detected\\n', '=VAL | explicit\\n', '=VAL >detected\\n', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_4RWC():
    yaml = '  [1, 2, 3]  \n  '
    expected = ['+STR', '+DOC', '+SEQ []', '=VAL :1', '=VAL :2', '=VAL :3', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_4UYU():
    yaml = '"foo: bar\\": baz"\n'
    expected = ['+STR', '+DOC', '=VAL "foo: bar": baz', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_4V8U():
    yaml = '---\nplain\\value\\with\\backslashes\n'
    expected = ['+STR', '+DOC ---', '=VAL :plain\\\\value\\\\with\\\\backslashes', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_4WA9():
    yaml = '- aaa: |2\n    xxx\n  bbb: |\n    xxx\n'
    expected = ['+STR', '+DOC', '+SEQ', '+MAP', '=VAL :aaa', '=VAL |xxx\\n', '=VAL :bbb', '=VAL |xxx\\n', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_4ZYM():
    yaml = 'plain: text\n  lines\nquoted: "text\n  \tlines"\nblock: |\n  text\n   \tlines\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :plain', '=VAL :text lines', '=VAL :quoted', '=VAL "text lines', '=VAL :block', '=VAL |text\\n \\tlines\\n', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
