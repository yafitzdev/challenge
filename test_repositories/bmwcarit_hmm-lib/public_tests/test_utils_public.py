import pytest
import math
from bmwcarit_hmm import utils

def test_normalize_probabilities_different():
    probs = {"orange": 4.0, "banana": 6.0}
    norm = utils.normalize_probabilities(probs)
    assert abs(norm["orange"] - 0.4) < 1e-10
    assert abs(norm["banana"] - 0.6) < 1e-10
    # Check original map not modified
    assert abs(probs["orange"] - 4.0) < 1e-10
    assert abs(probs["banana"] - 6.0) < 1e-10

def test_normalize_empty_different():
    with pytest.raises(ValueError):
        utils.normalize_probabilities({})

def test_normalize_null_value_different():
    with pytest.raises(TypeError):
        p = {"something": None}
        utils.normalize_probabilities(p)

def test_sum_different_values():
    l = [2.5, 3.0, 7.5]
    assert abs(utils.sum_(l) - 13.0) < 1e-10

def test_log2_different_inputs():
    assert abs(utils.log2(2.0) - 1.0) < 1e-10
    assert abs(utils.log2(4.0) - 2.0) < 1e-10
    assert abs(utils.log2(1.0) - 0.0) < 1e-10

def test_log2_zero_different():
    with pytest.raises(ValueError):
        utils.log2(0.0)

def test_log2_negative_different():
    with pytest.raises(ValueError):
        utils.log2(-2.0)

def test_log_sum_exp_list_different():
    d = [math.log(2.0), math.log(10.0)]
    expected = math.log(2.0 + 10.0)
    assert abs(utils.log_sum_exp(d) - expected) < 1e-10

def test_log_sum_exp_array_different():
    arr = [math.log(5), math.log(3)]
    expected = math.log(5.0 + 3.0)
    assert abs(utils.log_sum_exp(arr) - expected) < 1e-10