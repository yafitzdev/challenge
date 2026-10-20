import pytest
from collections import defaultdict

# The classes below are stubs and must be implemented in your src/ directory.
# Here they are imported as if available.
from src.awslabs_route53_infima import (
    SingleCellLattice,
    OneDimensionalLattice,
    TwoDimensionalLattice,
    SimpleSignatureShuffleSharder,
    Lattice,
)

def test_single_cell_simple_signature_shuffle_sharder():
    # Use a single cell lattice with 20 endpoints for a very simple test
    endpoints = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
        "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"
    ]
    lattice = SingleCellLattice()
    lattice.add_endpoints(endpoints)

    sharder = SimpleSignatureShuffleSharder(5353)

    # Compute 10,000 different shards and count how often each letter is observed
    count_by_letter = defaultdict(int)
    for i in range(10000):
        shard = sharder.shuffle_shard(lattice, str(i).encode(), 4)
        assert len(shard.get_all_endpoints()) == 4
        assert len(shard.get_dimensionality()) == 1
        assert len(shard.get_all_coordinates()) == 1

        for letter in shard.get_all_endpoints():
            count_by_letter[letter] += 1

    # Check that all 20 letters were seen
    assert len(count_by_letter.keys()) == 20

    # Each is expected to be seen 40,000 / 20 == 2,000. Check that we're within 10%
    for letter in count_by_letter:
        assert pytest.approx(count_by_letter[letter] / 2000.0, rel=0.1) == 1.0

def test_one_dimensional_simple_signature_shuffle_sharder():
    # Use a 1-D lattice with 20 endpoints for a very simple test
    endpointsA = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    endpointsB = ["K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"]

    lattice = OneDimensionalLattice("AZ")
    lattice.add_endpoints("us-east-1a", endpointsA)
    lattice.add_endpoints("us-east-1b", endpointsB)

    sharder = SimpleSignatureShuffleSharder(5353)

    count_by_letter = defaultdict(int)
    for i in range(100000):
        shard = sharder.shuffle_shard(lattice, str(i).encode(), 2)
        assert len(shard.get_all_endpoints()) == 4
        assert len(shard.get_dimensionality()) == 1
        assert len(shard.get_all_coordinates()) == 2

        for letter in shard.get_all_endpoints():
            count_by_letter[letter] += 1

        # Confirm endpoints stay in their own cells
        for letter in shard.get_endpoints_for_sector(["us-east-1a"]):
            assert letter in endpointsA
        for letter in shard.get_endpoints_for_sector(["us-east-1b"]):
            assert letter in endpointsB

    assert len(count_by_letter.keys()) == 20

    for letter in count_by_letter:
        assert pytest.approx(count_by_letter[letter] / 20000.0, rel=0.1) == 1.0

def test_two_dimensional_simple_signature_shuffle_sharder():
    endpointsA1 = ["A", "B", "C", "D", "E"]
    endpointsA2 = ["F", "G", "H", "I", "J"]
    endpointsB1 = ["K", "L", "M", "N", "O"]
    endpointsB2 = ["P", "Q", "R", "S", "T"]

    lattice = TwoDimensionalLattice("AZ", "Version")
    lattice.add_endpoints("us-east-1a", "1", endpointsA1)
    lattice.add_endpoints("us-east-1a", "2", endpointsA2)
    lattice.add_endpoints("us-east-1b", "1", endpointsB1)
    lattice.add_endpoints("us-east-1b", "2", endpointsB2)

    sharder = SimpleSignatureShuffleSharder(5353)
    count_by_letter = defaultdict(int)
    for i in range(10000):
        shard = sharder.shuffle_shard(lattice, str(i).encode(), 2)
        assert len(shard.get_all_endpoints()) == 4
        assert len(shard.get_dimensionality()) == 2
        assert len(shard.get_all_coordinates()) == 2

        for letter in shard.get_all_endpoints():
            count_by_letter[letter] += 1

        # Confirm endpoints stay in their own cells
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

    assert len(count_by_letter.keys()) == 20

    for letter in count_by_letter:
        assert pytest.approx(count_by_letter[letter] / 2000.0, rel=0.1) == 1.0

def test_asymmetrical_two_dimensional_simple_signature_shuffle_sharder():
    endpointsA1 = ["A", "B", "C", "D"]
    endpointsA2 = ["E", "F", "G", "H"]
    endpointsA3 = ["I", "J", "K", "L"]
    endpointsB1 = ["M", "N", "O", "P"]
    endpointsB2 = ["Q", "R", "S", "T"]
    endpointsB3 = ["U", "V", "W", "X"]

    lattice = TwoDimensionalLattice("AZ", "Version")
    lattice.add_endpoints("us-east-1a", "1", endpointsA1)
    lattice.add_endpoints("us-east-1a", "2", endpointsA2)
    lattice.add_endpoints("us-east-1a", "3", endpointsA3)
    lattice.add_endpoints("us-east-1b", "1", endpointsB1)
    lattice.add_endpoints("us-east-1b", "2", endpointsB2)
    lattice.add_endpoints("us-east-1b", "3", endpointsB3)

    sharder = SimpleSignatureShuffleSharder(5353)
    count_by_letter = defaultdict(int)
    for i in range(10000):
        shard = sharder.shuffle_shard(lattice, str(i).encode(), 2)
        assert len(shard.get_all_endpoints()) == 4
        assert len(shard.get_dimensionality()) == 2
        assert len(shard.get_all_coordinates()) == 2

        for letter in shard.get_all_endpoints():
            count_by_letter[letter] += 1

        sector_data = [
            (["us-east-1a", "1"], endpointsA1),
            (["us-east-1a", "2"], endpointsA2),
            (["us-east-1a", "3"], endpointsA3),
            (["us-east-1b", "1"], endpointsB1),
            (["us-east-1b", "2"], endpointsB2),
            (["us-east-1b", "3"], endpointsB3),
        ]
        for sector, group in sector_data:
            results = shard.get_endpoints_for_sector(sector)
            if results is not None:
                for letter in results:
                    assert letter in group

    assert len(count_by_letter.keys()) == 24

    for letter in count_by_letter:
        assert pytest.approx(count_by_letter[letter] / 1666.0, rel=0.1) == 1.0