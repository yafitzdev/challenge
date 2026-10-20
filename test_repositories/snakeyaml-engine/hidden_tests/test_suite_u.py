import pytest

from src.snakeyaml_engine import iter_events


def test_case_U3C3():
    yaml = '%TAG !yaml! tag:yaml.org,2002:\n---\n!yaml!str "foo"\n'
    expected = ['+STR', '+DOC ---', '=VAL <tag:yaml.org,2002:str> "foo', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_U3XV():
    yaml = '---\ntop1: &node1\n  &k1 key1: one\ntop2: &node2 # comment\n  key2: two\ntop3:\n  &k3 key3: three\ntop4:\n  &node4\n  &k4 key4: four\ntop5:\n  &node5\n  key5: five\ntop6: &val6\n  six\ntop7:\n  &val7 seven\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :top1', '+MAP &node1', '=VAL &k1 :key1', '=VAL :one', '-MAP', '=VAL :top2', '+MAP &node2', '=VAL :key2', '=VAL :two', '-MAP', '=VAL :top3', '+MAP', '=VAL &k3 :key3', '=VAL :three', '-MAP', '=VAL :top4', '+MAP &node4', '=VAL &k4 :key4', '=VAL :four', '-MAP', '=VAL :top5', '+MAP &node5', '=VAL :key5', '=VAL :five', '-MAP', '=VAL :top6', '=VAL &val6 :six', '=VAL :top7', '=VAL &val7 :seven', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_U44R():
    yaml = 'map:\n  key1: "quoted1"\n   key2: "bad indentation"\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :map', '+MAP', '=VAL :key1', '=VAL "quoted1']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_U99R():
    yaml = '- !!str, xxx\n'
    expected = ['+STR', '+DOC', '+SEQ']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_U9NS():
    yaml = '---\ntime: 20:03:20\nplayer: Sammy Sosa\naction: strike (miss)\n...\n---\ntime: 20:03:47\nplayer: Sammy Sosa\naction: grand slam\n...\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :time', '=VAL :20:03:20', '=VAL :player', '=VAL :Sammy Sosa', '=VAL :action', '=VAL :strike (miss)', '-MAP', '-DOC ...', '+DOC ---', '+MAP', '=VAL :time', '=VAL :20:03:47', '=VAL :player', '=VAL :Sammy Sosa', '=VAL :action', '=VAL :grand slam', '-MAP', '-DOC ...', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_UDM2():
    yaml = '- { url: http://example.org }\n'
    expected = ['+STR', '+DOC', '+SEQ', '+MAP {}', '=VAL :url', '=VAL :http://example.org', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_UDR7():
    yaml = 'sequence: [ one, two, ]\nmapping: { sky: blue, sea: green }\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :sequence', '+SEQ []', '=VAL :one', '=VAL :two', '-SEQ', '=VAL :mapping', '+MAP {}', '=VAL :sky', '=VAL :blue', '=VAL :sea', '=VAL :green', '-MAP', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_UGM3():
    yaml = '--- !<tag:clarkevans.com,2002:invoice>\ninvoice: 34843\ndate   : 2001-01-23\nbill-to: &id001\n    given  : Chris\n    family : Dumars\n    address:\n        lines: |\n            458 Walkman Dr.\n            Suite #292\n        city    : Royal Oak\n        state   : MI\n        postal  : 48046\nship-to: *id001\nproduct:\n    - sku         : BL394D\n      quantity    : 4\n      description : Basketball\n      price       : 450.00\n    - sku         : BL4438H\n      quantity    : 1\n      description : Super Hoop\n      price       : 2392.00\ntax  : 251.42\ntotal: 4443.52\ncomments:\n    Late afternoon is best.\n    Backup contact is Nancy\n    Billsmer @ 338-4338.\n'
    expected = ['+STR', '+DOC ---', '+MAP <tag:clarkevans.com,2002:invoice>', '=VAL :invoice', '=VAL :34843', '=VAL :date', '=VAL :2001-01-23', '=VAL :bill-to', '+MAP &id001', '=VAL :given', '=VAL :Chris', '=VAL :family', '=VAL :Dumars', '=VAL :address', '+MAP', '=VAL :lines', '=VAL |458 Walkman Dr.\\nSuite #292\\n', '=VAL :city', '=VAL :Royal Oak', '=VAL :state', '=VAL :MI', '=VAL :postal', '=VAL :48046', '-MAP', '-MAP', '=VAL :ship-to', '=ALI *id001', '=VAL :product', '+SEQ', '+MAP', '=VAL :sku', '=VAL :BL394D', '=VAL :quantity', '=VAL :4', '=VAL :description', '=VAL :Basketball', '=VAL :price', '=VAL :450.00', '-MAP', '+MAP', '=VAL :sku', '=VAL :BL4438H', '=VAL :quantity', '=VAL :1', '=VAL :description', '=VAL :Super Hoop', '=VAL :price', '=VAL :2392.00', '-MAP', '-SEQ', '=VAL :tax', '=VAL :251.42', '=VAL :total', '=VAL :4443.52', '=VAL :comments', '=VAL :Late afternoon is best. Backup contact is Nancy Billsmer @ 338-4338.', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_UKK6_00():
    yaml = '- :\n'
    expected = ['+STR', '+DOC', '+SEQ', '+MAP']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_UKK6_02():
    yaml = '!\n'
    expected = ['+STR', '+DOC', '=VAL <!> :', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_UT92():
    yaml = '---\n{ matches\n% : 20 }\n...\n---\n# Empty\n...\n'
    expected = ['+STR', '+DOC ---', '+MAP {}', '=VAL :matches %', '=VAL :']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected


def test_case_UV7Q():
    yaml = 'x:\n - x\n  \tx\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :x', '+SEQ', '=VAL :x']
    events = []
    with pytest.raises(Exception):
        for event in iter_events(yaml):
            events.append(event)
    assert events == expected
