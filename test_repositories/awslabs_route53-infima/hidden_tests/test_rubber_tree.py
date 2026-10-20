from src.awslabs_route53_infima.util import HealthCheckedResourceRecord
from src.awslabs_route53_infima import SingleCellLattice, TwoDimensionalLattice, RubberTree

def test_small_rubber_tree():
    endpoints = ["A", "B", "C", "D", "E", "F", "G", "H"]
    lattice = SingleCellLattice()
    for endpoint in endpoints:
        hcrr = HealthCheckedResourceRecord(endpoint, endpoint)
        lattice.add_endpoint(hcrr)
    rrs = RubberTree.vulcanize("Z124", "www.example.com", "TXT", 60, lattice, 8)
    assert len(rrs) == 64

def test_big_rubber_tree():
    endpoints = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
        "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"
    ]
    lattice = SingleCellLattice()
    for endpoint in endpoints:
        hcrr = HealthCheckedResourceRecord(endpoint, endpoint)
        lattice.add_endpoint(hcrr)
    rrs = RubberTree.vulcanize("Z124", "www.example.com", "TXT", 60, lattice, 8)
    assert len(rrs) == 160

def test_two_dimensional_rubber_tree():
    endpointsA1 = ["A", "B", "C", "D", "E"]
    endpointsA2 = ["F", "G", "H", "I", "J"]
    endpointsB1 = ["K", "L", "M", "N", "O"]
    endpointsB2 = ["P", "Q", "R", "S", "T"]
    lattice = TwoDimensionalLattice("AZ", "Version")
    for endpoint in endpointsA1:
        hcrr = HealthCheckedResourceRecord(endpoint, endpoint)
        lattice.add_endpoint("us-east-1a", "1", hcrr)
    for endpoint in endpointsA2:
        hcrr = HealthCheckedResourceRecord(endpoint, endpoint)
        lattice.add_endpoint("us-east-1a", "2", hcrr)
    for endpoint in endpointsB1:
        hcrr = HealthCheckedResourceRecord(endpoint, endpoint)
        lattice.add_endpoint("us-east-1b", "1", hcrr)
    for endpoint in endpointsB2:
        hcrr = HealthCheckedResourceRecord(endpoint, endpoint)
        lattice.add_endpoint("us-east-1b", "2", hcrr)
    rrs = RubberTree.vulcanize("Z124", "www.example.com", "TXT", 60, lattice, 8)
    assert len(rrs) == 485