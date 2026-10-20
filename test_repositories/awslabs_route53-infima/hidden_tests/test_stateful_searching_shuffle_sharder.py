import pytest
from collections import defaultdict

from src.awslabs_route53_infima import (
    SingleCellLattice,
    OneDimensionalLattice,
    TwoDimensionalLattice,
    StatefulSearchingShuffleSharder,
    Lattice,
)

class MockFragmentStore:
    def __init__(self):
        self.store = set()
    def save_fragment(self, fragment):
        key = tuple(sorted(fragment))
        self.store.add(key)
    def is_fragment_used(self, fragment):
        key = tuple(sorted(fragment))
        return key in self.store

def test_overlap_stateful_searching_shuffle_sharder():
    endpoints = ["A", "B", "C", "D", "E"]
    lattice = SingleCellLattice()
    lattice.add_endpoints(endpoints)
    mock_store = MockFragmentStore()
    sharder = StatefulSearchingShuffleSharder(mock_store)
    for i in range(2):
        try:
            sharder.shuffle_shard(lattice, 4, 2)
            if i == 1:
                pytest.fail("Only 1 valid shard")
        except Exception:
            if i != 1:
                pytest.fail()

def test_single_cell_stateful_searching_shuffle_sharder():
    endpoints = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
        "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"
    ]
    lattice = SingleCellLattice()
    lattice.add_endpoints(endpoints)
    mock_store = MockFragmentStore()
    sharder = StatefulSearchingShuffleSharder(mock_store)
    count_by_letter = defaultdict(int)
    for i in range(100):
        shard = sharder.shuffle_shard(lattice, 4, 2)
        assert len(shard.get_all_endpoints()) == 4
        assert len(shard.get_dimensionality()) == 1
        assert len(shard.get_all_coordinates()) == 1
        for letter in shard.get_all_endpoints():
            count_by_letter[letter] += 1
    assert len(count_by_letter) == 20

def test_one_dimensional_simple_signature_shuffle_sharder_stateful():
    endpointsA = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    endpointsB = ["K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"]
    lattice = OneDimensionalLattice("AZ")
    lattice.add_endpoints("us-east-1a", endpointsA)
    lattice.add_endpoints("us-east-1b", endpointsB)
    sharder = StatefulSearchingShuffleSharder(MockFragmentStore())
    count_by_letter = defaultdict(int)
    for i in range(45):
        shard = sharder.shuffle_shard(lattice, 2, 2)
        assert len(shard.get_all_endpoints()) == 4
        assert len(shard.get_dimensionality()) == 1
        assert len(shard.get_all_coordinates()) == 2
        for letter in shard.get_all_endpoints():
            count_by_letter[letter] += 1
        for letter in shard.get_endpoints_for_sector(["us-east-1a"]):
            assert letter in endpointsA
        for letter in shard.get_endpoints_for_sector(["us-east-1b"]):
            assert letter in endpointsB
    assert len(count_by_letter) == 20

def test_two_dimensional_simple_signature_shuffle_sharder_stateful():
    endpointsA1 = ["A", "B", "C", "D", "E"]
    endpointsA2 = ["F", "G", "H", "I", "J"]
    endpointsB1 = ["K", "L", "M", "N", "O"]
    endpointsB2 = ["P", "Q", "R", "S", "T"]
    lattice = TwoDimensionalLattice("AZ", "Version")
    lattice.add_endpoints("us-east-1a", "1", endpointsA1)
    lattice.add_endpoints("us-east-1a", "2", endpointsA2)
    lattice.add_endpoints("us-east-1b", "1", endpointsB1)
    lattice.add_endpoints("us-east-1b", "2", endpointsB2)
    sharder = StatefulSearchingShuffleSharder(MockFragmentStore())
    count_by_letter = defaultdict(int)
    for i in range(20):
        shard = sharder.shuffle_shard(lattice, 2, 2)
        assert len(shard.get_all_endpoints()) == 4
        assert len(shard.get_dimensionality()) == 2
        assert len(shard.get_all_coordinates()) == 2
        for letter in shard.get_all_endpoints():
            count_by_letter[letter] += 1
        for sector, group in [
            (["us-east-1a", "1"], endpointsA1),
            (["us-east-1a", "2"], endpointsA2),
            (["us-east-1b", "1"], endpointsB1),
            (["us-east-1b", "2"], endpointsB2),
        ]:
            results = shard.get_endpoints_for_sector(sector)
            if results is not None:
                for letter in results:
                    assert letter in group
    assert len(count_by_letter) == 20