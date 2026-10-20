import pytest

from src.snakeyaml_engine import iter_events


def test_case_735Y():
    yaml = '-\n  "flow in block"\n- >\n Block scalar\n- !!map # Block collection\n  foo : bar\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL "flow in block', '=VAL >Block scalar\\n', '+MAP <tag:yaml.org,2002:map>', '=VAL :foo', '=VAL :bar', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_74H7():
    yaml = '!!str a: b\nc: !!int 42\ne: !!str f\ng: h\n!!str 23: !!bool false\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL <tag:yaml.org,2002:str> :a', '=VAL :b', '=VAL :c', '=VAL <tag:yaml.org,2002:int> :42', '=VAL :e', '=VAL <tag:yaml.org,2002:str> :f', '=VAL :g', '=VAL :h', '=VAL <tag:yaml.org,2002:str> :23', '=VAL <tag:yaml.org,2002:bool> :false', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_753E():
    yaml = '--- |-\n ab\n \n \n...\n'
    expected = ['+STR', '+DOC ---', '=VAL |ab', '-DOC ...', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_7A4E():
    yaml = '" 1st non-empty\n\n 2nd non-empty \n\t3rd non-empty "\n'
    expected = ['+STR', '+DOC', '=VAL " 1st non-empty\\n2nd non-empty 3rd non-empty ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_7BMT():
    yaml = '---\ntop1: &node1\n  &k1 key1: one\ntop2: &node2 # comment\n  key2: two\ntop3:\n  &k3 key3: three\ntop4: &node4\n  &k4 key4: four\ntop5: &node5\n  key5: five\ntop6: &val6\n  six\ntop7:\n  &val7 seven\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :top1', '+MAP &node1', '=VAL &k1 :key1', '=VAL :one', '-MAP', '=VAL :top2', '+MAP &node2', '=VAL :key2', '=VAL :two', '-MAP', '=VAL :top3', '+MAP', '=VAL &k3 :key3', '=VAL :three', '-MAP', '=VAL :top4', '+MAP &node4', '=VAL &k4 :key4', '=VAL :four', '-MAP', '=VAL :top5', '+MAP &node5', '=VAL :key5', '=VAL :five', '-MAP', '=VAL :top6', '=VAL &val6 :six', '=VAL :top7', '=VAL &val7 :seven', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_7BUB():
    yaml = '---\nhr:\n  - Mark McGwire\n  # Following node labeled SS\n  - &SS Sammy Sosa\nrbi:\n  - *SS # Subsequent occurrence\n  - Ken Griffey\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :hr', '+SEQ', '=VAL :Mark McGwire', '=VAL &SS :Sammy Sosa', '-SEQ', '=VAL :rbi', '+SEQ', '=ALI *SS', '=VAL :Ken Griffey', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_7FWL():
    yaml = '!<tag:yaml.org,2002:str> foo :\n  !<!bar> baz\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL <tag:yaml.org,2002:str> :foo', '=VAL <!bar> :baz', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_7LBH():
    yaml = '"a\\nb": 1\n"c\n d": 1\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL "a\\nb', '=VAL :1']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_7MNF():
    yaml = 'top1:\n  key1: val1\ntop2\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :top1', '+MAP', '=VAL :key1', '=VAL :val1']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_7TMG():
    yaml = '---\n[ word1\n# comment\n, word2]\n'
    expected = ['+STR', '+DOC ---', '+SEQ []', '=VAL :word1', '=VAL :word2', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_7W2P():
    yaml = '? a\n? b\nc:\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :a', '=VAL :', '=VAL :b', '=VAL :', '=VAL :c', '=VAL :', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_7Z25():
    yaml = '---\nscalar1\n...\nkey: value\n'
    expected = ['+STR', '+DOC ---', '=VAL :scalar1', '-DOC ...']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_7ZZ5():
    yaml = '---\nnested sequences:\n- - - []\n- - - {}\nkey1: []\nkey2: {}\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :nested sequences', '+SEQ', '+SEQ', '+SEQ', '+SEQ []', '-SEQ', '-SEQ', '-SEQ', '+SEQ', '+SEQ', '+MAP {}', '-MAP', '-SEQ', '-SEQ', '-SEQ', '=VAL :key1', '+SEQ []', '-SEQ', '=VAL :key2', '+MAP {}', '-MAP', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
