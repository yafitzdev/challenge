from src.awslabs_route53_infima import TwoDimensionalLattice

def test_constructor_and_dimension_names():
    lattice = TwoDimensionalLattice("D1", "D2")
    assert lattice.get_dimension_names() == ["D1", "D2"]

def test_add_endpoints_and_get_endpoints():
    lattice = TwoDimensionalLattice("X", "Y")
    lattice.add_endpoints("a", "b", ["foo", "bar"])
    assert set(lattice.get_endpoints("a", "b")) == set(["foo", "bar"])

def test_add_endpoint():
    lattice = TwoDimensionalLattice("A", "B")
    lattice.add_endpoint("X", "Y", "Z")
    assert set(lattice.get_endpoints("X", "Y")) == set(["Z"])

def test_get_endpoints_not_present():
    lattice = TwoDimensionalLattice("DD1", "DD2")
    assert lattice.get_endpoints("no", "key") == []