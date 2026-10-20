class JavaList(list):
    """A list whose string form matches java.util.AbstractCollection.toString()."""

    def __str__(self):
        return "[" + ", ".join(str(e) for e in self) + "]"


class _SubListIterator:
    def __init__(self, master_list, sub_list_size):
        self._master = master_list
        self._size = sub_list_size
        if sub_list_size > len(master_list):
            raise ValueError("subListSize must be <= master list size. %d > %d"
                             % (sub_list_size, len(master_list)))
        self._cursors = list(range(sub_list_size))

    def __iter__(self):
        return self

    def has_next(self):
        # cursors[0] in Java; a zero-sized cursor array would throw there
        return self._cursors[0] <= (len(self._master) - len(self._cursors))

    def __next__(self):
        if not self.has_next():
            raise StopIteration
        cursors = self._cursors
        sub = JavaList(self._master[i] for i in cursors)
        n = len(cursors)
        size = len(self._master)
        reset = False
        for i in range(n):
            if reset:
                cursors[i] = cursors[i - 1] + 1
            elif i + 1 < n and cursors[i + 1] == size - (n - (i + 1)):
                cursors[i] += 1
                reset = True
            elif i == n - 1:
                cursors[i] += 1
        return sub


class IterableSubListGenerator:
    """Generates every sub list of size sub_list_size of master_list."""

    def __init__(self, master_list, sub_list_size):
        self._master = master_list
        self._size = sub_list_size

    def __iter__(self):
        return _SubListIterator(list(self._master), self._size)

    iterator = __iter__
