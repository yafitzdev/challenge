import functools

from src.awslabs_route53_model import ResourceRecord


@functools.total_ordering
class ComparableResourceRecord(ResourceRecord):
    def __init__(self, value):
        super().__init__(value)

    def compare_to(self, other):
        a, b = self.get_value(), other.get_value()
        return (a > b) - (a < b)

    def __lt__(self, other):
        return self.compare_to(other) < 0

    def __eq__(self, other):
        return ResourceRecord.__eq__(self, other)

    def __hash__(self):
        return ResourceRecord.__hash__(self)
