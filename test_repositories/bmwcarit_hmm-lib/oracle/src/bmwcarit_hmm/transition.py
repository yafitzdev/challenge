class Transition(object):
    """Represents the transition between two consecutive candidates."""

    def __init__(self, from_candidate, to_candidate):
        self.from_candidate = from_candidate
        self.to_candidate = to_candidate

    # Java-style aliases
    @property
    def fromCandidate(self):
        return self.from_candidate

    @property
    def toCandidate(self):
        return self.to_candidate

    def __hash__(self):
        return hash((self.from_candidate, self.to_candidate))

    def __eq__(self, other):
        if self is other:
            return True
        if other is None:
            return False
        if type(self) is not type(other):
            return False
        return self.from_candidate == other.from_candidate and self.to_candidate == other.to_candidate

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "Transition [fromCandidate=" + str(self.from_candidate) + ", toCandidate=" + \
            str(self.to_candidate) + "]"

    __repr__ = __str__
