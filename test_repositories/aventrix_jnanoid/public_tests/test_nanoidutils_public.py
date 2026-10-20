import pytest
import random
from src.jnanoid.nano_id_utils import NanoIdUtils

def char_array_to_string(arr):
    if isinstance(arr, str):
        return arr
    return ''.join(arr)

def test_random_nanoid_noargs_length_and_alphabet():
    nanoid = NanoIdUtils.randomNanoId()
    assert nanoid is not None
    # Default length is 21
    assert len(nanoid) == 21

    default_alphabet_str = char_array_to_string(NanoIdUtils.DEFAULT_ALPHABET)
    for c in nanoid:
        assert c in default_alphabet_str

def test_random_nanoid_custom_alphabet_public():
    custom_alphabet = ['a', 'B', '4', '!']
    rng = random.SystemRandom()
    size = 13
    nanoid = NanoIdUtils.randomNanoId(rng, custom_alphabet, size)
    assert nanoid is not None
    assert len(nanoid) == size
    alphabet_str = char_array_to_string(custom_alphabet)
    for c in nanoid:
        assert c in alphabet_str

def test_random_nanoid_null_alphabet_public():
    rng = random.SystemRandom()
    with pytest.raises(ValueError):
        NanoIdUtils.randomNanoId(rng, None, 10)

def test_random_nanoid_empty_alphabet_public():
    rng = random.SystemRandom()
    with pytest.raises(ValueError):
        NanoIdUtils.randomNanoId(rng, [], 8)

def test_random_nanoid_too_short_length_public():
    alphabet = ['a', 'b']
    rng = random.SystemRandom()
    with pytest.raises(ValueError):
        NanoIdUtils.randomNanoId(rng, alphabet, 0)

def test_random_nanoid_negative_length_public():
    alphabet = ['a', 'b', 'c']
    rng = random.SystemRandom()
    with pytest.raises(ValueError):
        NanoIdUtils.randomNanoId(rng, alphabet, -5)

def test_random_nanoid_alphabet_too_long_public():
    alphabet = [chr(32 + (i % 94)) for i in range(300)]
    rng = random.SystemRandom()
    with pytest.raises(ValueError):
        NanoIdUtils.randomNanoId(rng, alphabet, 8)

def test_random_nanoid_custom_random_public():
    predictable_random = random.Random(42)
    alphabet = ['Q', 'W', 'E']
    size = 6
    nanoid = NanoIdUtils.randomNanoId(predictable_random, alphabet, size)
    assert len(nanoid) == size
    alphabet_str = char_array_to_string(alphabet)
    for c in nanoid:
        assert c in alphabet_str
    # Deterministic - should match second call with same seed
    expected = NanoIdUtils.randomNanoId(random.Random(42), alphabet, size)
    assert expected == nanoid

def test_random_nanoid_default_random_public():
    length = 17
    rng = random.SystemRandom()
    default_alphabet = NanoIdUtils.DEFAULT_ALPHABET
    nanoid = NanoIdUtils.randomNanoId(rng, default_alphabet, length)
    assert len(nanoid) == length
    default_alphabet_str = char_array_to_string(default_alphabet)
    for c in nanoid:
        assert c in default_alphabet_str