import hashlib

from .lattice import Lattice
from .java_random import JavaRandom, java_shuffle


def _sub_list(lst, end):
    if end > len(lst) or end < 0:
        raise IndexError("toIndex = %d" % end)
    return lst[:end]


class SimpleSignatureShuffleSharder:
    def __init__(self, seed):
        self._seed = seed

    def shuffle_shard(self, lattice, identifier, endpoints_per_cell):
        chosen = Lattice(lattice.get_dimension_names())

        digest = hashlib.md5()
        digest.update(str(self._seed).encode())
        if isinstance(identifier, str):
            identifier = identifier.encode()
        digest.update(bytes(identifier))
        checksum = digest.digest()

        shard_seed = 0
        for i in range(8):
            shard_seed += (checksum[i] & 0xFF) << (8 * i)
        shard_seed &= (1 << 64) - 1

        entropy = JavaRandom(shard_seed)

        shuffled_dimension_values = []
        for dimension_name in lattice.get_dimension_names():
            shuffled = list(lattice.get_dimension_values(dimension_name))
            java_shuffle(shuffled, entropy)
            shuffled_dimension_values.append(shuffled)

        dimensionality = lattice.get_dimensionality()

        if len(lattice.get_dimensionality()) == 1:
            for value in shuffled_dimension_values[0]:
                available = list(lattice.get_endpoints_for_sector([value]))
                java_shuffle(available, entropy)
                chosen.add_endpoints_for_sector([value], _sub_list(available, endpoints_per_cell))
            return chosen

        minimum_dimension_size = 2 ** 31 - 1
        for size in dimensionality.values():
            if size < minimum_dimension_size:
                minimum_dimension_size = size

        for _ in range(minimum_dimension_size):
            coordinates = []
            for j in range(len(lattice.get_dimension_names())):
                coordinates.append(shuffled_dimension_values[j].pop(0))
            available = list(lattice.get_endpoints_for_sector(coordinates))
            java_shuffle(available, entropy)
            chosen.add_endpoints_for_sector(coordinates, _sub_list(available, endpoints_per_cell))
        return chosen
