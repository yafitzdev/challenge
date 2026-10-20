import pytest
import math
from bmwcarit_hmm import utils

def test_initial_hash_map_capacity():
    assert utils.initial_hash_map_capacity(10) == 14

def test_log_to_non_log_probabilities():
    log_probs = {"A": math.log(0.4), "B": math.log(0.6)}
    probs = utils.log_to_non_log_probabilities(log_probs)
    assert abs(probs["A"] - 0.4) < 1e-10
    assert abs(probs["B"] - 0.6) < 1e-10

def test_probability_in_range():
    assert utils.probability_in_range(1.0, 1e-8)
    assert utils.probability_in_range(0.0, 1e-8)
    assert not utils.probability_in_range(-0.01, 1e-4)
    assert utils.probability_in_range(1.000009, 1e-3)
    assert not utils.probability_in_range(1.2, 1e-4)