from bmwcarit_hmm.transition import Transition

def test_equals_and_hash_code_public():
    t1 = Transition("X", "Y")
    t2 = Transition("X", "Y")
    t3 = Transition("Y", "Z")
    t4 = Transition("X", "Z")
    assert t1 == t2
    assert hash(t1) == hash(t2)
    assert t1 != t3
    assert hash(t1) != hash(t3)
    assert t1 != t4

def test_equals_with_nulls_public():
    t1 = Transition(None, "Y")
    t2 = Transition(None, "Y")
    t3 = Transition("X", None)
    t4 = Transition(None, None)
    t5 = Transition(None, None)
    assert t1 == t2
    assert t4 == t5
    assert t1 != t3

def test_to_string_public():
    t = Transition("Q", "P")
    assert "fromCandidate=Q" in str(t)
    assert "toCandidate=P" in str(t)

def test_not_equals_other_types_and_null_public():
    t = Transition("I", "J")
    assert t != None
    assert t != 12345