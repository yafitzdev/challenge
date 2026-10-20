"""Port of com.bmw.hmm.Utils."""
import math


def initial_hash_map_capacity(max_elements):
    # Default load factor of HashMaps is 0.75
    return int(max_elements / 0.75) + 1


def log_to_non_log_probabilities(log_probabilities):
    result = {}
    for key, value in log_probabilities.items():
        result[key] = math.exp(value)
    return result


def probability_in_range(probability, delta):
    """Note that complex probabilities are not checked."""
    return -delta <= probability <= 1.0 + delta
