import pytest
from bmwcarit_hmm.transition import Transition

def test_equals_and_hash_code():
    t1 = Transition("A", "B")
    t2 = Transition("A", "B")
    t3 = Transition("B", "A")
    t4 = Transition("A", "C")
    assert t1 == t2
    assert hash(t1) == hash(t2)
    assert t1 != t3
    assert hash(t1) != hash(t3)
    assert t1 != t4

def test_equals_with_nulls():
    t1 = Transition(None, "B")
    t2 = Transition(None, "B")
    t3 = Transition("A", None)
    t4 = Transition(None, None)
    t5 = Transition(None, None)

    assert t1 == t2
    assert t4 == t5
    assert t1 != t3

def test_to_string():
    t = Transition("A", "B")
    assert "fromCandidate=A" in str(t)
    assert "toCandidate=B" in str(t)

def test_not_equals_other_types_and_null():
    t = Transition("A", "B")
    assert t != None
    assert t != "not_a_transition"