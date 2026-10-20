import pytest

from src.awslabs_route53_infima import Lattice

def test_single_cell_lattice():
    SingleCellLattice = getattr(__import__('src.awslabs_route53_infima', fromlist=['SingleCellLattice']), 'SingleCellLattice')
    lattice = SingleCellLattice()
    lattice.add_endpoint("A")
    lattice.add_endpoints(["B", "C", "D"])
    # Check all endpoints in, with ordering
    assert str(lattice.get_all_endpoints()) == "['B', 'C', 'D', 'A']"

def test_one_dimensional_lattice():
    OneDimensionalLattice = getattr(__import__('src.awslabs_route53_infima', fromlist=['OneDimensionalLattice']), 'OneDimensionalLattice')
    endpointsA = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    endpointsB = ["K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"]

    lattice = OneDimensionalLattice("AZ")
    lattice.add_endpoints("us-east-1a", endpointsA)
    lattice.add_endpoints("us-east-1b", endpointsB)
    assert len(lattice.get_all_endpoints()) == 20
    assert len(lattice.simulate_failure("AZ", "us-east-1a").get_all_endpoints()) == 10
    assert len(lattice.simulate_failure("AZ", "us-east-1b").get_all_endpoints()) == 10

def test_two_dimensional_lattice():
    TwoDimensionalLattice = getattr(__import__('src.awslabs_route53_infima', fromlist=['TwoDimensionalLattice']), 'TwoDimensionalLattice')
    endpointsA1 = ["A", "B", "C", "D", "E"]
    endpointsA2 = ["F", "G", "H", "I", "J"]
    endpointsB1 = ["K", "L", "M", "N", "O"]
    endpointsB2 = ["P", "Q", "R", "S", "T"]

    lattice = TwoDimensionalLattice("AZ", "Version")
    lattice.add_endpoints("us-east-1a", "1", endpointsA1)
    lattice.add_endpoints("us-east-1a", "2", endpointsA2)
    lattice.add_endpoints("us-east-1b", "1", endpointsB1)
    lattice.add_endpoints("us-east-1b", "2", endpointsB2)

    assert len(lattice.get_all_endpoints()) == 20
    assert len(lattice.simulate_failure("AZ", "us-east-1a").get_all_endpoints()) == 10
    assert len(lattice.simulate_failure("AZ", "us-east-1b").get_all_endpoints()) == 10
    assert len(lattice.simulate_failure("Version", "1").get_all_endpoints()) == 10
    assert len(lattice.simulate_failure("Version", "2").get_all_endpoints()) == 10
    assert len(lattice.simulate_failure("AZ", "us-east-1a").simulate_failure("Version", "1").get_all_endpoints()) == 5
    assert len(lattice.simulate_failure("AZ", "us-east-1a").simulate_failure("Version", "2").get_all_endpoints()) == 5
    assert len(lattice.simulate_failure("AZ", "us-east-1b").simulate_failure("Version", "1").get_all_endpoints()) == 5
    assert len(lattice.simulate_failure("AZ", "us-east-1b").simulate_failure("Version", "2").get_all_endpoints()) == 5