import pytest

from src.snakeyaml_engine import iter_events


def test_case_229Q():
    yaml = '-\n  name: Mark McGwire\n  hr:   65\n  avg:  0.278\n-\n  name: Sammy Sosa\n  hr:   63\n  avg:  0.288\n'
    expected = ['+STR', '+DOC', '+SEQ', '+MAP', '=VAL :name', '=VAL :Mark McGwire', '=VAL :hr', '=VAL :65', '=VAL :avg', '=VAL :0.278', '-MAP', '+MAP', '=VAL :name', '=VAL :Sammy Sosa', '=VAL :hr', '=VAL :63', '=VAL :avg', '=VAL :0.288', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_236B():
    yaml = 'foo:\n  bar\ninvalid\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '=VAL :bar']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_26DV():
    yaml = '"top1" : \n  "key1" : &alias1 scalar1\n\'top2\' : \n  \'key2\' : &alias2 scalar2\ntop3: &node3 \n  *alias1 : scalar3\ntop4: \n  *alias2 : scalar4\ntop5   :    \n  scalar5\ntop6: \n  &anchor6 \'key6\' : scalar6\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL "top1', '+MAP', '=VAL "key1', '=VAL &alias1 :scalar1', '-MAP', "=VAL 'top2", '+MAP', "=VAL 'key2", '=VAL &alias2 :scalar2', '-MAP', '=VAL :top3', '+MAP &node3', '=ALI *alias1', '=VAL :scalar3', '-MAP', '=VAL :top4', '+MAP', '=ALI *alias2', '=VAL :scalar4', '-MAP', '=VAL :top5', '=VAL :scalar5', '=VAL :top6', '+MAP', "=VAL &anchor6 'key6", '=VAL :scalar6', '-MAP', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_27NA():
    yaml = '%YAML 1.2\n--- text\n'
    expected = ['+STR', '+DOC ---', '=VAL :text', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_2AUY():
    yaml = ' - !!str a\n - b\n - !!int 42\n - d\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL <tag:yaml.org,2002:str> :a', '=VAL :b', '=VAL <tag:yaml.org,2002:int> :42', '=VAL :d', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_2CMS():
    yaml = 'this\n is\n  invalid: x\n'
    expected = ['+STR', '+DOC', '=VAL :this is invalid']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_2EBW():
    yaml = 'a!"#$%&\'()*+,-./09:;<=>?@AZ[\\]^_`az{|}~: safe\n?foo: safe question mark\n:foo: safe colon\n-foo: safe dash\nthis is#not: a comment\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :a!"#$%&\'()*+,-./09:;<=>?@AZ[\\\\]^_`az{|}~', '=VAL :safe', '=VAL :?foo', '=VAL :safe question mark', '=VAL ::foo', '=VAL :safe colon', '=VAL :-foo', '=VAL :safe dash', '=VAL :this is#not', '=VAL :a comment', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_2G84_00():
    yaml = '--- |0\n'
    expected = ['+STR', '+DOC ---']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_2G84_01():
    yaml = '--- |10\n'
    expected = ['+STR', '+DOC ---']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_2G84_03():
    yaml = '--- |1+'
    expected = ['+STR', '+DOC ---', '=VAL |', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_2JQS():
    yaml = ': a\n: b\n'
    expected = ['+STR', '+DOC', '+MAP']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_2LFX():
    yaml = '%FOO  bar baz # Should be ignored\n              # with a warning.\n---\n"foo"\n'
    expected = ['+STR', '+DOC ---', '=VAL "foo', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_2SXE():
    yaml = '&a: key: &a value\nfoo:\n  *a:\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL &a: :key', '=VAL &a :value', '=VAL :foo', '=ALI *a:', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_2XXW():
    yaml = '# Sets are represented as a\n# Mapping where each key is\n# associated with a null value\n--- !!set\n? Mark McGwire\n? Sammy Sosa\n? Ken Griff\n'
    expected = ['+STR', '+DOC ---', '+MAP <tag:yaml.org,2002:set>', '=VAL :Mark McGwire', '=VAL :', '=VAL :Sammy Sosa', '=VAL :', '=VAL :Ken Griff', '=VAL :', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
