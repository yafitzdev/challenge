import random

from .lattice import Lattice
from .util.iterable_sub_list_generator import IterableSubListGenerator


class NoShardsAvailableException(Exception):
    pass


class FragmentStore:
    """Interface for a list-based fragment store."""

    def save_fragment(self, fragment):
        raise NotImplementedError

    def is_fragment_used(self, fragment):
        raise NotImplementedError


class StatefulSearchingShuffleSharder:
    NoShardsAvailableException = NoShardsAvailableException
    FragmentStore = FragmentStore

    def __init__(self, store):
        self._store = store

    def shuffle_shard(self, lattice, endpoints_per_cell, maximum_overlap):
        shard = self._helper(lattice, endpoints_per_cell, maximum_overlap)
        if len(shard.get_all_endpoints()) == 0:
            raise NoShardsAvailableException()
        for fragment in IterableSubListGenerator(shard.get_all_endpoints(), maximum_overlap + 1):
            self._store.save_fragment(fragment)
        return shard

    def _helper(self, lattice, endpoints_per_cell, maximum_overlap):
        all_coordinates = [list(c) for c in lattice.get_all_coordinates()]
        all_coordinates.sort()
        random.shuffle(all_coordinates)
        for coordinate in all_coordinates:
            compliment = lattice
            for i in range(len(lattice.get_dimensionality())):
                compliment = compliment.simulate_failure(lattice.get_dimension_name(i), coordinate[i])
            endpoints = list(lattice.get_endpoints_for_sector(coordinate))
            random.shuffle(endpoints)
            for fragment in IterableSubListGenerator(endpoints, endpoints_per_cell):
                if len(fragment) >= maximum_overlap and self._too_many_collisions(fragment, maximum_overlap):
                    continue
                picked = self._helper(compliment, endpoints_per_cell, maximum_overlap)
                combined = list(fragment)
                combined.extend(picked.get_all_endpoints())
                if len(combined) >= maximum_overlap and self._too_many_collisions(combined, maximum_overlap):
                    continue
                picked.add_endpoints_for_sector(coordinate, fragment)
                return picked
        return Lattice(lattice.get_dimension_names())

    def _too_many_collisions(self, haystack, maximum_overlap):
        if len(haystack) <= maximum_overlap:
            return False
        elif len(haystack) == maximum_overlap + 1:
            return self._store.is_fragment_used(haystack)
        for fragment in IterableSubListGenerator(haystack, maximum_overlap + 1):
            if self._store.is_fragment_used(fragment):
                return True
        return False
