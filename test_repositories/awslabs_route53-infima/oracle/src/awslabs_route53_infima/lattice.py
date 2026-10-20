class Lattice:
    """An n-dimensional lattice of endpoints, keyed by sector coordinates."""

    def __init__(self, dimension_names):
        if len(dimension_names) == 0:
            raise ValueError("At least one dimension is required")
        self._dimension_names = dimension_names
        # dimension name -> insertion-ordered set of values
        self._values_by_dimension = {name: {} for name in dimension_names}
        # tuple(coordinate) -> list of endpoints; iterated in sorted (TreeMap) order
        self._endpoints_by_coordinate = {}

    def _sorted_coordinates(self):
        return sorted(self._endpoints_by_coordinate.keys())

    def add_endpoints_for_sector(self, sector_coordinates, endpoints):
        if len(sector_coordinates) != len(self._dimension_names):
            raise ValueError("Mismatch between dimensions of lattice and sector")
        key = tuple(sector_coordinates)
        to_be_added = list(endpoints)
        existing = self._endpoints_by_coordinate.get(key)
        if existing is not None:
            to_be_added.extend(existing)
        self._endpoints_by_coordinate[key] = to_be_added
        for i, name in enumerate(self._dimension_names):
            self._values_by_dimension[name][sector_coordinates[i]] = None

    def get_endpoints_for_sector(self, sector_coordinates):
        if len(sector_coordinates) != len(self._dimension_names):
            raise ValueError("Mismatch between dimensions of lattice and sector")
        return self._endpoints_by_coordinate.get(tuple(sector_coordinates))

    def get_all_endpoints(self):
        all_endpoints = []
        for key in self._sorted_coordinates():
            all_endpoints.extend(self._endpoints_by_coordinate[key])
        return all_endpoints

    def get_all_coordinates(self):
        return set(self._endpoints_by_coordinate.keys())

    def get_dimensionality(self):
        return {name: len(self.get_dimension_values(name)) for name in self._dimension_names}

    def get_dimension_names(self):
        return self._dimension_names

    def get_dimension_name(self, dimension):
        return self._dimension_names[dimension]

    def get_dimension_values(self, dimension_name):
        values = self._values_by_dimension.get(dimension_name)
        return None if values is None else values.keys()

    def get_dimension_size(self, dimension_name):
        return len(self._values_by_dimension[dimension_name])

    def simulate_failure(self, dimension_name, dimension_value):
        sublattice = Lattice(self._dimension_names)
        try:
            dimension_number = list(self._dimension_names).index(dimension_name)
        except ValueError:
            raise ValueError("Unknown dimension name")
        for key in self._sorted_coordinates():
            if key[dimension_number] != dimension_value:
                sublattice.add_endpoints_for_sector(list(key), self._endpoints_by_coordinate[key])
        return sublattice

    def __str__(self):
        sep = "\n"
        sb = "[" + " , ".join(self._dimension_names) + "]" + sep
        for key in self._sorted_coordinates():
            sb += "[" + " , ".join(key[i] for i in range(len(self._dimension_names))) + "] -> ["
            sb += " , ".join(str(e) for e in self._endpoints_by_coordinate[key])
            sb += "]" + sep
        return sb


class OneDimensionalLattice(Lattice):
    def __init__(self, dimension_x_name="AvailabilityZone"):
        super().__init__([dimension_x_name])

    def add_endpoints(self, dimension_x_coord, endpoints):
        self.add_endpoints_for_sector([dimension_x_coord], endpoints)

    def get_endpoints(self, dimension_x_coord):
        return self.get_endpoints_for_sector([dimension_x_coord])

    def add_endpoint(self, dimension_x_coord, endpoint):
        self.add_endpoints(dimension_x_coord, [endpoint])


class SingleCellLattice(OneDimensionalLattice):
    DIMENSION = "DimensionX"

    def __init__(self, endpoints=None):
        super().__init__(SingleCellLattice.DIMENSION)
        if endpoints is not None:
            OneDimensionalLattice.add_endpoints(self, SingleCellLattice.DIMENSION, endpoints)

    def add_endpoints(self, *args):
        # Java overloads: addEndpoints(Collection) and inherited addEndpoints(String, Collection)
        if len(args) == 1:
            OneDimensionalLattice.add_endpoints(self, SingleCellLattice.DIMENSION, args[0])
        else:
            OneDimensionalLattice.add_endpoints(self, *args)

    def add_endpoint(self, *args):
        if len(args) == 1:
            self.add_endpoints([args[0]])
        else:
            OneDimensionalLattice.add_endpoint(self, *args)

    def get_endpoints(self, *args):
        if len(args) == 0:
            return OneDimensionalLattice.get_endpoints(self, SingleCellLattice.DIMENSION)
        return OneDimensionalLattice.get_endpoints(self, *args)


class TwoDimensionalLattice(Lattice):
    def __init__(self, dimension_x_name, dimension_y_name):
        super().__init__([dimension_x_name, dimension_y_name])

    def add_endpoints(self, dimension_x_coord, dimension_y_coord, endpoints):
        self.add_endpoints_for_sector([dimension_x_coord, dimension_y_coord], endpoints)

    def add_endpoint(self, dimension_x_coord, dimension_y_coord, endpoint):
        self.add_endpoints(dimension_x_coord, dimension_y_coord, [endpoint])

    def get_endpoints(self, dimension_x_coord, dimension_y_coord):
        return self.get_endpoints_for_sector([dimension_x_coord, dimension_y_coord])
