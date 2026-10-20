import pytest

from src.snakeyaml_engine import iter_events


def test_case_Y2GN():
    yaml = '---\nkey: &an:chor value\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :key', '=VAL &an:chor :value', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_Y79Y_001():
    yaml = 'foo: |\n \t\nbar: 1\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :foo', '=VAL |\\t\\n', '=VAL :bar', '=VAL :1', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_Y79Y_002():
    yaml = '- [\n\t\n foo\n ]\n'
    expected = ['+STR', '+DOC', '+SEQ', '+SEQ []', '=VAL :foo', '-SEQ', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_Y79Y_003():
    yaml = '- [\n\tfoo,\n foo\n ]\n'
    expected = ['+STR', '+DOC', '+SEQ', '+SEQ []', '=VAL :foo', '=VAL :foo', '-SEQ', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_Y79Y_004():
    yaml = '-\t-\n'
    expected = ['+STR', '+DOC', '+SEQ']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_Y79Y_005():
    yaml = '- \t-\n'
    expected = ['+STR', '+DOC', '+SEQ']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_Y79Y_006():
    yaml = '?\t-\n'
    expected = ['+STR', '+DOC', '+MAP']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_Y79Y_007():
    yaml = '? -\n:\t-\n'
    expected = ['+STR', '+DOC', '+MAP', '+SEQ', '=VAL :', '-SEQ']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_Y79Y_008():
    yaml = '?\tkey:\n'
    expected = ['+STR', '+DOC', '+MAP']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_Y79Y_009():
    yaml = '? key:\n:\tkey:\n'
    expected = ['+STR', '+DOC', '+MAP', '+MAP', '=VAL :key', '=VAL :', '-MAP']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_YD5X():
    yaml = '- [name        , hr, avg  ]\n- [Mark McGwire, 65, 0.278]\n- [Sammy Sosa  , 63, 0.288]\n'
    expected = ['+STR', '+DOC', '+SEQ', '+SEQ []', '=VAL :name', '=VAL :hr', '=VAL :avg', '-SEQ', '+SEQ []', '=VAL :Mark McGwire', '=VAL :65', '=VAL :0.278', '-SEQ', '+SEQ []', '=VAL :Sammy Sosa', '=VAL :63', '=VAL :0.288', '-SEQ', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_YJV2():
    yaml = '[-]\n'
    expected = ['+STR']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected
