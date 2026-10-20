import pytest
import random
import string
from src.jnanoid.nano_id_utils import NanoIdUtils

def test_default_random_nanoid():
    nanoid = NanoIdUtils.randomNanoId()
    assert nanoid is not None
    assert len(nanoid) == NanoIdUtils.DEFAULT_SIZE
    # Should only contain characters in the default alphabet
    default_alphabet_str = ''.join(NanoIdUtils.DEFAULT_ALPHABET)
    for c in nanoid:
        assert c in default_alphabet_str

def test_random_nanoid_with_custom_size():
    length = 10
    nanoid = NanoIdUtils.randomNanoId(random.SystemRandom(), NanoIdUtils.DEFAULT_ALPHABET, length)
    assert nanoid is not None
    assert len(nanoid) == length

def test_random_nanoid_with_min_max_size():
    length = 1
    nanoid = NanoIdUtils.randomNanoId(random.SystemRandom(), NanoIdUtils.DEFAULT_ALPHABET, length)
    assert len(nanoid) == length

    length = 1024
    nanoid = NanoIdUtils.randomNanoId(random.SystemRandom(), NanoIdUtils.DEFAULT_ALPHABET, length)
    assert len(nanoid) == length

def test_random_nanoid_zero_size():
    with pytest.raises(ValueError):
        NanoIdUtils.randomNanoId(random.SystemRandom(), NanoIdUtils.DEFAULT_ALPHABET, 0)

def test_random_nanoid_negative_size():
    with pytest.raises(ValueError):
        NanoIdUtils.randomNanoId(random.SystemRandom(), NanoIdUtils.DEFAULT_ALPHABET, -1)

def test_random_nanoid_null_random():
    with pytest.raises(ValueError):
        NanoIdUtils.randomNanoId(None, NanoIdUtils.DEFAULT_ALPHABET, 10)

def test_random_nanoid_null_alphabet():
    with pytest.raises(ValueError):
        NanoIdUtils.randomNanoId(random.SystemRandom(), None, 10)

def test_random_nanoid_empty_alphabet():
    with pytest.raises(ValueError):
        NanoIdUtils.randomNanoId(random.SystemRandom(), [], 10)

def test_random_nanoid_oversized_alphabet():
    big_alphabet = [chr(ord('a') + (i % 26)) for i in range(256)]
    with pytest.raises(ValueError):
        NanoIdUtils.randomNanoId(random.SystemRandom(), big_alphabet, 10)

def test_nanoid_is_url_friendly():
    nanoid = NanoIdUtils.randomNanoId()
    assert NanoIdUtils.is_url_friendly(nanoid)

def test_nanoidutils_private_constructor(monkeypatch):
    # Python: just ensure instantiating the class works
    try:
        instance = NanoIdUtils()
    except Exception as e:
        pytest.fail("NanoIdUtils() constructor raised Exception: %s" % e)

def test_random_nanoid_with_non_default_random():
    rng = random.Random(1234)
    nanoid = NanoIdUtils.randomNanoId(rng, NanoIdUtils.DEFAULT_ALPHABET, 11)
    assert nanoid is not None
    assert len(nanoid) == 11

def test_random_nanoid_with_small_alphabet():
    alphabet = ['a', 'b']
    nanoid = NanoIdUtils.randomNanoId(random.SystemRandom(), alphabet, 6)
    assert len(nanoid) == 6
    for c in nanoid:
        assert c in alphabet

def test_nanoid_uniqueness():
    nanoid1 = NanoIdUtils.randomNanoId()
    nanoid2 = NanoIdUtils.randomNanoId()
    assert nanoid1 != nanoid2  # Extremely unlikely for default size + default alphabet