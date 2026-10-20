from src.awslabs_route53_infima import TwoDimensionalLattice

def test_add_and_get_endpoints_different_data():
    lattice = TwoDimensionalLattice("rack", "slot")
    lattice.add_endpoints("rack-17", "slot-9", ["R", "S", "T"])
    found = lattice.get_endpoints("rack-17", "slot-9")
    assert "R" in found
    assert "S" in found
    assert "T" in found

def test_add_endpoint_different_data():
    lattice = TwoDimensionalLattice("zoneA", "rowB")
    lattice.add_endpoint("foo", "bar", "X")
    found = lattice.get_endpoints("foo", "bar")
    assert "X" in found
    assert len(found) == 1

def test_get_endpoints_for_nonexistent_coordinates_public():
    lattice = TwoDimensionalLattice("c", "d")
    assert lattice.get_endpoints("doesnot", "exist") == []

def test_dimension_names_public():
    lattice = TwoDimensionalLattice("fruit", "color")
    assert lattice.get_dimension_names() == ["fruit", "color"]