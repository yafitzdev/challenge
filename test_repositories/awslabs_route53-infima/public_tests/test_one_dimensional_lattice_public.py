from src.awslabs_route53_infima import OneDimensionalLattice

def test_constructor_with_name_different():
    lattice = OneDimensionalLattice("ZoneX")
    assert lattice is not None
    assert lattice.get_dimension_names() == ["ZoneX"]

def test_default_constructor_public():
    lattice = OneDimensionalLattice()
    assert lattice is not None
    assert lattice.get_dimension_names() == ["AvailabilityZone"]

def test_add_and_get_endpoints_different_data():
    lattice = OneDimensionalLattice()
    lattice.add_endpoints("eu-central-1b", ["M", "N"])
    result = lattice.get_endpoints("eu-central-1b")
    assert "M" in result
    assert "N" in result

def test_add_endpoint_different_data():
    lattice = OneDimensionalLattice()
    lattice.add_endpoint("eu-north-1", "Bar")
    res = lattice.get_endpoints("eu-north-1")
    assert len(res) == 1
    assert "Bar" in res

def test_empty_endpoints_public():
    lattice = OneDimensionalLattice()
    assert lattice.get_endpoints("doesnotexist") == []