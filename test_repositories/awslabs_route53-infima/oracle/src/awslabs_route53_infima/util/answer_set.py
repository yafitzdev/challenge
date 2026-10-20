import bisect
import hashlib

from src.awslabs_route53_model import AliasTarget, ResourceRecordSet
from .health_checked_resource_record import HealthCheckedResourceRecord


def _to_base36(n):
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    if n == 0:
        return "0"
    neg = n < 0
    n = -n if neg else n
    out = []
    while n:
        n, r = divmod(n, 36)
        out.append(digits[r])
    return ("-" if neg else "") + "".join(reversed(out))


def _jstr(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v)


class AnswerSet:
    """Sorted set of ComparableResourceRecord (port of a java.util.TreeSet subclass)."""

    def __init__(self, records=None):
        self._items = []
        if records is not None:
            self.add_all(records)

    # --- TreeSet behaviour ---
    def add(self, record):
        idx = bisect.bisect_left(self._items, record)
        if idx < len(self._items) and self._items[idx].compare_to(record) == 0:
            return False
        self._items.insert(idx, record)
        return True

    def add_all(self, records):
        changed = False
        for r in records:
            changed = self.add(r) or changed
        return changed

    addAll = add_all

    def __iter__(self):
        return iter(list(self._items))

    def __len__(self):
        return len(self._items)

    def size(self):
        return len(self._items)

    def __contains__(self, item):
        idx = bisect.bisect_left(self._items, item)
        return idx < len(self._items) and self._items[idx].compare_to(item) == 0

    def to_array(self, array=None):
        if array is None or len(array) < len(self._items):
            return list(self._items)
        for i, item in enumerate(self._items):
            array[i] = item
        if len(array) > len(self._items):
            array[len(self._items)] = None
        return array

    # --- Infima ---
    def to_resource_record_sets(self, hosted_zone_id, name, type, ttl):
        rrs_list = []
        healthcheck_ids = set()
        rrs = []
        for crr in self._items:
            if isinstance(crr, HealthCheckedResourceRecord):
                healthcheck_ids.update(crr.get_healthcheck_ids())
            rrs.append(crr)

        leaf = ResourceRecordSet()
        leaf.set_type(type)
        leaf.set_ttl(ttl)
        leaf.set_resource_records(rrs)
        leaf.set_weight(1)
        leaf.set_set_identifier("leafnode")
        leaf.set_name(name)

        remaining = sorted(healthcheck_ids)
        if remaining:
            leaf.set_health_check_id(remaining.pop(0))
        rrs_list.append(leaf)
        if not remaining:
            return rrs_list

        entry = leaf
        while remaining:
            alias = ResourceRecordSet()
            target = AliasTarget()
            checksum = self._checksum_resource_record_set_data(entry)
            alias.set_name(entry.get_name())
            alias.set_type(entry.get_type())
            alias.set_weight(entry.get_weight())
            alias.set_health_check_id(remaining.pop(0))
            target_name = checksum + "." + entry.get_name()
            entry.set_name(target_name)
            target.set_dns_name(target_name)
            target.set_evaluate_target_health(True)
            target.set_hosted_zone_id(hosted_zone_id)
            alias.set_set_identifier("Alias to " + checksum)
            alias.set_alias_target(target)
            rrs_list.append(alias)
            entry = alias
        return rrs_list

    @staticmethod
    def _checksum_resource_record_set_data(rr):
        digest = hashlib.md5()
        digest.update(rr.get_type().encode("utf-8"))
        if rr.get_alias_target() is not None:
            at = rr.get_alias_target()
            digest.update(at.get_hosted_zone_id().encode("utf-8"))
            digest.update(at.get_dns_name().encode("utf-8"))
            digest.update(_jstr(at.get_evaluate_target_health()).encode("utf-8"))
        else:
            records = "[" + ", ".join(str(r) for r in rr.get_resource_records()) + "]"
            digest.update(records.encode("utf-8"))
            digest.update(_jstr(rr.get_ttl()).encode("utf-8"))
        bi = int.from_bytes(digest.digest(), "big", signed=True)
        return _to_base36(bi)
