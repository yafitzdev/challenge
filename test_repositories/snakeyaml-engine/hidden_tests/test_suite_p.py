import pytest

from src.snakeyaml_engine import iter_events


def test_case_P2AD():
    yaml = '- | # Empty header↓\n literal\n- >1 # Indentation indicator↓\n  folded\n- |+ # Chomping indicator↓\n keep\n\n- >1- # Both indicators↓\n  strip\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL |literal\\n', '=VAL > folded\\n', '=VAL |keep\\n\\n', '=VAL > strip', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_P76L():
    yaml = '%TAG !! tag:example.com,2000:app/\n---\n!!int 1 - 3 # Interval, not integer\n'
    expected = ['+STR', '+DOC ---', '=VAL <tag:example.com,2000:app/int> :1 - 3', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_P94K():
    yaml = 'key:    # Comment\n        # lines\n  value\n\n\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :key', '=VAL :value', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_PBJ2():
    yaml = 'american:\n  - Boston Red Sox\n  - Detroit Tigers\n  - New York Yankees\nnational:\n  - New York Mets\n  - Chicago Cubs\n  - Atlanta Braves\n'
    expected = ['+STR', '+DOC', '+MAP', '=VAL :american', '+SEQ', '=VAL :Boston Red Sox', '=VAL :Detroit Tigers', '=VAL :New York Yankees', '-SEQ', '=VAL :national', '+SEQ', '=VAL :New York Mets', '=VAL :Chicago Cubs', '=VAL :Atlanta Braves', '-SEQ', '-MAP', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_PRH3():
    yaml = "' 1st non-empty\n\n 2nd non-empty \n\t3rd non-empty '\n"
    expected = ['+STR', '+DOC', "=VAL ' 1st non-empty\\n2nd non-empty 3rd non-empty ", '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_PUW8():
    yaml = '---\na: b\n---\n'
    expected = ['+STR', '+DOC ---', '+MAP', '=VAL :a', '=VAL :b', '-MAP', '-DOC', '+DOC ---', '=VAL :', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected


def test_case_PW8X():
    yaml = '- &a\n- a\n-\n  &a : a\n  b: &b\n-\n  &c : &a\n-\n  ? &d\n-\n  ? &e\n  : &a\n'
    expected = ['+STR', '+DOC', '+SEQ', '=VAL &a :', '=VAL :a', '+MAP', '=VAL &a :', '=VAL :a', '=VAL :b', '=VAL &b :', '-MAP', '+MAP', '=VAL &c :', '=VAL &a :', '-MAP', '+MAP', '=VAL &d :', '=VAL :', '-MAP', '+MAP', '=VAL &e :', '=VAL &a :', '-MAP', '-SEQ', '-DOC', '-STR']
    events = []
    for event in iter_events(yaml):
        events.append(event)
    assert events == expected
