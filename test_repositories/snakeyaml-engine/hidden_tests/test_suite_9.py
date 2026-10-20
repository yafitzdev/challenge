import pytest

from src.snakeyaml_engine import iter_events


def test_case_93JH():
    yaml = ' - key: value\n   key2: value2\n -\n   key3: value3\n'
    expected = ['+STR', '+DOC', '+SEQ', '+MAP', '=VAL :key', '=VAL :value', '=VAL :key2', '=VAL :value2', '-MAP', '+MAP', '=VAL :key3', '=VAL :value3', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_93WF():
    yaml = '--- >-\n  trimmed\n  \n \n\n  as\n  space\n'
    expected = ['+STR', '+DOC ---', '=VAL >trimmed\\n\\n\\nas space', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_96L6():
    yaml = "--- >\n  Mark McGwire's\n  year was crippled\n  by a knee injury.\n"
    expected = ['+STR', '+DOC ---', "=VAL >Mark McGwire's year was crippled by a knee injury.\\n", '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_96NN_00():
    yaml = 'foo: |-\n \tbar\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '=VAL |\\tbar', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_96NN_01():
    yaml = 'foo: |-\n \tbar'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '=VAL |\\tbar', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_9BXH():
    yaml = '---\n- { "single line", a: b}\n- { "multi\n  line", a: b}\n'
    expected = ['+STR', '+DOC ---', '+SEQ', '+MAP {}', '=VAL "single line', '=VAL :', '=VAL :a', '=VAL :b', '-MAP', '+MAP {}', '=VAL "multi line', '=VAL :', '=VAL :a', '=VAL :b', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_9C9N():
    yaml = '---\nflow: [a,\nb,\nc]\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :flow', '+SEQ []', '=VAL :a', '=VAL :b', '=VAL :c', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_9CWY():
    yaml = 'key:\n - item1\n - item2\ninvalid\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key', '+SEQ', '=VAL :item1', '=VAL :item2']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_9DXL():
    yaml = 'Mapping: Document\n---\n# Empty\n...\n%YAML 1.2\n---\nmatches %: 20\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :Mapping', '=VAL :Document', '-MAP', '-DOC', '+DOC ---', '=VAL :', '-DOC ...', '+DOC ---', '+MAP', '=VAL :matches %', '=VAL :20', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_9FMG():
    yaml = 'a:\n  b:\n    c: d\n  e:\n    f: g\nh: i\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :a', '+MAP', '=VAL :b', '+MAP', '=VAL :c', '=VAL :d', '-MAP', '=VAL :e', '+MAP', '=VAL :f', '=VAL :g', '-MAP', '-MAP', '=VAL :h', '=VAL :i', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_9HCY():
    yaml = '!foo "bar"\n%TAG ! tag:example.com,2000:app/\n---\n!foo "bar"\n'
    expected = ['+STR', '+DOC', '=VAL <!foo> "bar']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_9J7A():
    yaml = 'foo:\n  bar: baz\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '+MAP', '=VAL :bar', '=VAL :baz', '-MAP', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_9JBA():
    yaml = '---\n[ a, b, c, ]#invalid\n'
    expected = ['+STR', '+DOC ---', '+SEQ []', '=VAL :a', '=VAL :b', '=VAL :c', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_9KAX():
    yaml = '---\n&a1\n!!str\nscalar1\n---\n!!str\n&a2\nscalar2\n---\n&a3\n!!str scalar3\n---\n&a4 !!map\n&a5 !!str key5: value4\n---\na6: 1\n&anchor6 b6: 2\n---\n!!map\n&a8 !!str key8: value7\n---\n!!map\n!!str &a10 key10: value9\n---\n!!str &a11\nvalue11\n'
    expected = ['+STR', '+DOC ---', '=VAL &a1 <tag:yaml.org,2002:str> :scalar1', '-DOC', '+DOC ---', '=VAL &a2 <tag:yaml.org,2002:str> :scalar2', '-DOC', '+DOC ---', '=VAL &a3 <tag:yaml.org,2002:str> :scalar3', '-DOC', '+DOC ---', '+MAP &a4 <tag:yaml.org,2002:map>', '=VAL &a5 <tag:yaml.org,2002:str> :key5', '=VAL :value4', '-MAP', '-DOC', '+DOC ---', '+MAP', '=VAL :a6', '=VAL :1', '=VAL &anchor6 :b6', '=VAL :2', '-MAP', '-DOC', '+DOC ---', '+MAP <tag:yaml.org,2002:map>', '=VAL &a8 <tag:yaml.org,2002:str> :key8', '=VAL :value7', '-MAP', '-DOC', '+DOC ---', '+MAP <tag:yaml.org,2002:map>', '=VAL &a10 <tag:yaml.org,2002:str> :key10', '=VAL :value9', '-MAP', '-DOC', '+DOC ---', '=VAL &a11 <tag:yaml.org,2002:str> :value11', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_9MAG():
    yaml = '---\n[ , a, b, c ]\n'
    expected = ['+STR', '+DOC ---', '+SEQ []']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_9MMA():
    yaml = '%YAML 1.2\n'
    expected = ['+STR']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_9MMW():
    yaml = '- [ YAML : separate ]\n- [ "JSON like":adjacent ]\n- [ {JSON: like}:adjacent ]\n'
    expected = ['+STR', '+DOC', '+SEQ', '+SEQ []', '+MAP {}', '=VAL :YAML', '=VAL :separate', '-MAP', '-SEQ', '+SEQ []', '+MAP {}', '=VAL "JSON like', '=VAL :adjacent', '-MAP', '-SEQ', '+SEQ []', '+MAP {}', '+MAP {}', '=VAL :JSON', '=VAL :like', '-MAP', '=VAL :adjacent', '-MAP', '-SEQ', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_9MQT_00():
    yaml = '--- "a\n...x\nb"\n'
    expected = ['+STR', '+DOC ---', '=VAL "a ...x b', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_9MQT_01():
    yaml = '--- "a\n... x\nb"\n'
    expected = ['+STR', '+DOC ---']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_9SA2():
    yaml = '---\n- { "single line": value}\n- { "multi\n  line": value}\n'
    expected = ['+STR', '+DOC ---', '+SEQ', '+MAP {}', '=VAL "single line', '=VAL :value', '-MAP', '+MAP {}', '=VAL "multi line', '=VAL :']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_9SHH():
    yaml = 'single: \'text\'\ndouble: "text"\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :single', "=VAL 'text", '=VAL :double', '=VAL "text', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_9TFX():
    yaml = '---\n" 1st non-empty\n\n 2nd non-empty \n 3rd non-empty "\n'
    expected = ['+STR', '+DOC ---', '=VAL " 1st non-empty\\n2nd non-empty 3rd non-empty ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_9U5K():
    yaml = '---\n# Products purchased\n- item    : Super Hoop\n  quantity: 1\n- item    : Basketball\n  quantity: 4\n- item    : Big Shoes\n  quantity: 1\n'
    expected = ['+STR', '+DOC ---', '+SEQ', '+MAP', '=VAL :item', '=VAL :Super Hoop', '=VAL :quantity', '=VAL :1', '-MAP', '+MAP', '=VAL :item', '=VAL :Basketball', '=VAL :quantity', '=VAL :4', '-MAP', '+MAP', '=VAL :item', '=VAL :Big Shoes', '=VAL :quantity', '=VAL :1', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_9YRD():
    yaml = 'a\nb  \n  c\nd\n\ne\n'
    expected = ['+STR', '+DOC', '=VAL :a b c d\\ne', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
