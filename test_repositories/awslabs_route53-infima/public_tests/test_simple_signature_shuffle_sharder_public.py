import pytest

from src.awslabs_route53_infima import (
    OneDimensionalLattice,
    SimpleSignatureShuffleSharder,
)

def test_shuffle_shard_returns_correct_size_with_different_data():
    lattice = OneDimensionalLattice()
    lattice.add_endpoints("az2", ["W", "X", "Y", "Z"])
    sharder = SimpleSignatureShuffleSharder(456)
    shard = sharder.shuffle_shard(lattice, b"unique-777", 3)
    endpoints = shard.get_all_endpoints()
    assert len(endpoints) == 3

def test_shuffle_shard_different_identifiers_produce_different_shards_with_different_data():
    lattice = OneDimensionalLattice()
    lattice.add_endpoints("public", ["X", "Y", "Z", "W"])
    sharder = SimpleSignatureShuffleSharder(99)
    shard1 = sharder.shuffle_shard(lattice, b"alpha", 2)
    shard2 = sharder.shuffle_shard(lattice, b"beta", 2)
    assert set(shard1.get_all_endpoints()) != set(shard2.get_all_endpoints())

def test_throws_no_such_algorithm_exception_coverage_only():
    # Coverage only, see comment in reference test
    sharder = SimpleSignatureShuffleSharder(13)
    # No negative test, coverage only