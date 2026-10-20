import pytest

from src.awslabs_route53_infima import Lattice

def test_construction_and_dimension_names_with_different_dims():
    dims = ["dimA", "dimB"]
    lattice = Lattice(dims)
    assert lattice.get_dimension_names() == dims

def test_add_endpoints_for_sector_and_get_endpoints_different():
    lattice = Lattice(["y"])
    coord = ["custom"]
    lattice.add_endpoints_for_sector(coord, ["P", "Q"])
    assert "P" in lattice.get_endpoints_for_sector(coord)
    assert "Q" in lattice.get_endpoints_for_sector(coord)

def test_simulate_failure_different_values():
    lattice = Lattice(["country", "city"])
    coord1 = ["Spain", "Madrid"]
    lattice.add_endpoints_for_sector(coord1, ["Server1", "Server2"])
    failed = lattice.simulate_failure("country", "Spain")
    assert not failed.get_all_endpoints() or not failed.get_endpoints_for_sector(["Spain", "Madrid"])

def test_get_dimension_values_and_dimensionality_public():
    lattice = Lattice(["continent", "region"])
    lattice.add_endpoints_for_sector(["Europe", "North"], ["HostA"])
    lattice.add_endpoints_for_sector(["Europe", "South"], ["HostB"])
    regions = set(lattice.get_dimension_values("region"))
    assert "North" in regions
    assert "South" in regions
    dims = lattice.get_dimensionality()
    assert len(dims) == 2

def test_equals_and_hash_code_different_data():
    l1 = Lattice(["R", "S"])
    l2 = Lattice(["R", "S"])
    l1.add_endpoints_for_sector(["foo", "bar"], ["baz"])
    l2.add_endpoints_for_sector(["foo", "bar"], ["baz"])
    assert l1 == l2
    assert hash(l1) == hash(l2)

def test_to_string_not_null_public():
    lattice = Lattice(["E"])
    assert lattice.__str__() is not None

def test_no_endpoints_public():
    lattice = Lattice(["F"])
    assert lattice.get_all_endpoints() == []