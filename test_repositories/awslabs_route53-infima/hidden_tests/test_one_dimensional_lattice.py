from src.awslabs_route53_infima import OneDimensionalLattice

def test_constructor_with_name():
    lattice = OneDimensionalLattice("Zone")
    assert lattice is not None
    assert lattice.get_dimension_names() == ["Zone"]

def test_default_constructor():
    lattice = OneDimensionalLattice()
    assert lattice is not None
    assert lattice.get_dimension_names() == ["AvailabilityZone"]

def test_add_and_get_endpoints():
    lattice = OneDimensionalLattice()
    lattice.add_endpoints("us-east-1a", ["A", "B"])
    result = lattice.get_endpoints("us-east-1a")
    assert "A" in result
    assert "B" in result

def test_add_endpoint():
    lattice = OneDimensionalLattice()
    lattice.add_endpoint("us-west-2", "Foo")
    res = lattice.get_endpoints("us-west-2")
    assert len(res) == 1
    assert "Foo" in res

def test_empty_endpoints():
    lattice = OneDimensionalLattice()
    assert lattice.get_endpoints("nonexistent") == []