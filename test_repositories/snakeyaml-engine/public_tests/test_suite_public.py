import pytest

from src.snakeyaml_engine import iter_events


def test_case_2G84_02():
    yaml = '--- |1-'
    expected = ['+STR', '+DOC ---', '=VAL |', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_3GZX():
    yaml = 'First occurrence: &anchor Foo\nSecond occurrence: *anchor\nOverride anchor: &anchor Bar\nReuse anchor: *anchor\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :First occurrence', '=VAL &anchor :Foo', '=VAL :Second occurrence', '=ALI *anchor', '=VAL :Override anchor', '=VAL &anchor :Bar', '=VAL :Reuse anchor', '=ALI *anchor', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_3UYS():
    yaml = 'escaped slash: "a\\/b"\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :escaped slash', '=VAL "a/b', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_4MUZ_01():
    yaml = '{"foo"\n: bar}\n'
    expected = ['+STR', '+DOC', '+MAP {}', '=VAL "foo', '=VAL :']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_54T7():
    yaml = '{foo: you, bar: far}\n'
    expected = ['+STR', '+DOC', '+MAP {}', '=VAL :foo', '=VAL :you', '=VAL :bar', '=VAL :far', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_5MUD():
    yaml = '---\n{ "foo"\n  :bar }\n'
    expected = ['+STR', '+DOC ---', '+MAP {}', '=VAL "foo', '=VAL :']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_6BCT():
    yaml = '- foo:\t bar\n- - baz\n  -\tbaz\n'
    expected = ['+STR', '+DOC', '+SEQ', '+MAP', '=VAL :foo', '=VAL :bar', '-MAP', '+SEQ', '=VAL :baz', '=VAL :baz', '-SEQ', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_6KGN():
    yaml = '---\na: &anchor\nb: *anchor\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :a', '=VAL &anchor :', '=VAL :b', '=ALI *anchor', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_6ZKB():
    yaml = 'Document\n---\n# Empty\n...\n%YAML 1.2\n---\nmatches %: 20\n'
    expected = ['+STR', '+DOC', '=VAL :Document', '-DOC', '+DOC ---', '=VAL :', '-DOC ...', '+DOC ---', '+MAP', '=VAL :matches %', '=VAL :20', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_7T8X():
    yaml = '>\n\n folded\n line\n\n next\n line\n   * bullet\n\n   * list\n   * lines\n\n last\n line\n\n# Comment\n'
    expected = ['+STR', '+DOC', '=VAL >\\nfolded line\\nnext line\\n  * bullet\\n\\n  * list\\n  * lines\\n\\nlast line\\n', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_8MK2():
    yaml = '! a\n'
    expected = ['+STR', '+DOC', '=VAL <!> :a', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_98YD():
    yaml = '# Comment only.\n'
    expected = ['+STR', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_9KBC():
    yaml = '--- key1: value1\n    key2: value2\n'
    expected = ['+STR', '+DOC ---', '=VAL :key1']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_9WXW():
    yaml = '# Private\n!foo "bar"\n...\n# Global\n%TAG ! tag:example.com,2000:app/\n---\n!foo "bar"\n'
    expected = ['+STR', '+DOC', '=VAL <!foo> "bar', '-DOC ...', '+DOC ---', '=VAL <tag:example.com,2000:app/foo> "bar', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_B63P():
    yaml = '%YAML 1.2\n...\n'
    expected = ['+STR']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_CFD4():
    yaml = '- [ : empty key ]\n- [: another empty key]\n'
    expected = ['+STR', '+DOC', '+SEQ', '+SEQ []']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_D49Q():
    yaml = "'a\\nb': 1\n'c\n d': 1\n"
    expected = ['+STR', '+DOC', '+MAP', "=VAL 'a\\\\nb", '=VAL :1']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_DE56_04():
    yaml = '"5 trailing\t\n    tab"\n'
    expected = ['+STR', '+DOC', '=VAL "5 trailing tab', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_DK95_04():
    yaml = 'foo: 1\n\t\nbar: 2\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '=VAL :1', '=VAL :bar', '=VAL :2', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_EW3V():
    yaml = 'k1: v1\n k2: v2\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :k1', '=VAL :v1 k2']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_FQ7F():
    yaml = '- Mark McGwire\n- Sammy Sosa\n- Ken Griffey\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL :Mark McGwire', '=VAL :Sammy Sosa', '=VAL :Ken Griffey', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_GH63():
    yaml = '? a\n: 1.3\nfifteen: d\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :a', '=VAL :1.3', '=VAL :fifteen', '=VAL :d', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_HRE5():
    yaml = '---\ndouble: "quoted \\\' scalar"\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :double']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_JEF9_01():
    yaml = '- |+\n   \n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL |\\n', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_K4SU():
    yaml = '- foo\n- bar\n- 42\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL :foo', '=VAL :bar', '=VAL :42', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_KSS4():
    yaml = '--- "quoted\nstring"\n--- &node foo\n'
    expected = ['+STR', '+DOC ---', '=VAL "quoted string', '-DOC', '+DOC ---', '=VAL &node :foo', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_LX3P():
    yaml = '[flow]: block\n'
    expected = ['+STR', '+DOC', '+MAP', '+SEQ []', '=VAL :flow', '-SEQ', '=VAL :block', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_MJS9():
    yaml = '>\n  foo \n \n  \t bar\n\n  baz\n'
    expected = ['+STR', '+DOC', '=VAL >foo \\n\\n\\t bar\\n\\nbaz\\n', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_MZX3():
    yaml = '- plain\n- "double quoted"\n- \'single quoted\'\n- >\n  block\n- plain again\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL :plain', '=VAL "double quoted', "=VAL 'single quoted", '=VAL >block\\n', '=VAL :plain again', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_P2EQ():
    yaml = '---\n- { y: z }- invalid\n'
    expected = ['+STR', '+DOC ---', '+SEQ']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_Q8AD():
    yaml = '---\n"folded \nto a space,\n \nto a line feed, or \t\\\n \\ \tnon-content"\n'
    expected = ['+STR', '+DOC ---', '=VAL "folded to a space,\\nto a line feed, or \\t \\tnon-content', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_RR7F():
    yaml = 'a: 4.2\n? d\n: 23\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :a', '=VAL :4.2', '=VAL :d', '=VAL :23', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_S98Z():
    yaml = 'empty block scalar: >\n \n  \n   \n # comment\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :empty block scalar']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_SU74():
    yaml = 'key1: &alias value1\n&b *alias : value2\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key1', '=VAL &alias :value1', '=VAL &b :', '=VAL :']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_TS54():
    yaml = '>\n ab\n cd\n \n ef\n\n\n gh\n'
    expected = ['+STR', '+DOC', '=VAL >ab cd\\nef\\n\\ngh\\n', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_UKK6_01():
    yaml = '::\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL ::', '=VAL :', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_W5VH():
    yaml = 'a: &:@*!$"<foo>: scalar a\nb: *:@*!$"<foo>:\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :a']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_Y79Y_000():
    yaml = 'foo: |\n\t\nbar: 1\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '=VAL |']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_Y79Y_010():
    yaml = '-\t-1\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL :-1', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_ZVH3():
    yaml = '- key: value\n - item1\n'
    expected = ['+STR', '+DOC', '+SEQ', '+MAP', '=VAL :key', '=VAL :value', '-MAP']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected
