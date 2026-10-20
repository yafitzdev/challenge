import pytest

from src.snakeyaml_engine import iter_events


def test_case_S3PD():
    yaml = 'plain key: in-line value\n: # Both empty\n"quoted key":\n- entry\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :plain key', '=VAL :in-line value']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_S4GJ():
    yaml = '---\nfolded: > first line\n  second line\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :folded']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_S4JQ():
    yaml = '# Assuming conventional resolution:\n- "12"\n- 12\n- ! 12\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL "12', '=VAL :12', '=VAL <!> :12', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_S4T7():
    yaml = 'aaa: bbb\n...\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :aaa', '=VAL :bbb', '-MAP', '-DOC ...', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_S7BG():
    yaml = '---\n- :,\n'
    expected = ['+STR', '+DOC ---', '+SEQ', '=VAL ::,', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_S9E8():
    yaml = 'sequence:\n- one\n- two\nmapping:\n  ? sky\n  : blue\n  sea : green\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :sequence', '+SEQ', '=VAL :one', '=VAL :two', '-SEQ', '=VAL :mapping', '+MAP', '=VAL :sky', '=VAL :blue', '=VAL :sea', '=VAL :green', '-MAP', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_SBG9():
    yaml = '{a: [b, c], [d, e]: f}\n'
    expected = ['+STR', '+DOC', '+MAP {}', '=VAL :a', '+SEQ []', '=VAL :b', '=VAL :c', '-SEQ', '+SEQ []', '=VAL :d', '=VAL :e', '-SEQ', '=VAL :f', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_SF5V():
    yaml = '%YAML 1.2\n%YAML 1.2\n---\n'
    expected = ['+STR']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_SKE5():
    yaml = '---\nseq:\n &anchor\n- a\n- b\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :seq', '+SEQ &anchor', '=VAL :a', '=VAL :b', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_SM9W_00():
    yaml = '-'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL :', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_SM9W_01():
    yaml = ':'
    expected = ['+STR', '+DOC', '+MAP']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_SR86():
    yaml = 'key1: &a value\nkey2: &b *a\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key1', '=VAL &a :value', '=VAL :key2', '=VAL &b :']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_SSW6():
    yaml = '---\n\'here\'\'s to "quotes"\'\n'
    expected = ['+STR', '+DOC ---', '=VAL \'here\'s to "quotes"', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_SU5Z():
    yaml = 'key: "value"# invalid comment\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key', '=VAL "value', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_SY6V():
    yaml = '&anchor - sequence entry\n'
    expected = ['+STR']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_SYW4():
    yaml = 'hr:  65    # Home runs\navg: 0.278 # Batting average\nrbi: 147   # Runs Batted In\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :hr', '=VAL :65', '=VAL :avg', '=VAL :0.278', '=VAL :rbi', '=VAL :147', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
