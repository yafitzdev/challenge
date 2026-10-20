"""Minimal port of the com.amazonaws.services.route53.model classes used by Infima."""


class ResourceRecord:
    def __init__(self, value=None):
        self._value = value

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, ResourceRecord):
            return NotImplemented
        return self._value == other._value

    def __hash__(self):
        return hash(self._value)

    def __str__(self):
        sb = "{"
        if self._value is not None:
            sb += "Value: " + str(self._value)
        sb += "}"
        return sb

    __repr__ = __str__


class AliasTarget:
    def __init__(self, hosted_zone_id=None, dns_name=None):
        self._hosted_zone_id = hosted_zone_id
        self._dns_name = dns_name
        self._evaluate_target_health = None

    def get_hosted_zone_id(self):
        return self._hosted_zone_id

    def set_hosted_zone_id(self, v):
        self._hosted_zone_id = v

    def get_dns_name(self):
        return self._dns_name

    def set_dns_name(self, v):
        self._dns_name = v

    def get_evaluate_target_health(self):
        return self._evaluate_target_health

    def set_evaluate_target_health(self, v):
        self._evaluate_target_health = v

    def __str__(self):
        parts = []
        if self._hosted_zone_id is not None:
            parts.append("HostedZoneId: " + str(self._hosted_zone_id))
        if self._dns_name is not None:
            parts.append("DNSName: " + str(self._dns_name))
        if self._evaluate_target_health is not None:
            parts.append("EvaluateTargetHealth: " + _jstr(self._evaluate_target_health))
        return "{" + ",".join(parts) + "}"

    __repr__ = __str__


def _jstr(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v)


class ResourceRecordSet:
    def __init__(self, name=None, type=None):
        self._name = name
        self._type = type
        self._set_identifier = None
        self._weight = None
        self._ttl = None
        self._resource_records = None
        self._alias_target = None
        self._health_check_id = None

    def get_name(self):
        return self._name

    def set_name(self, v):
        self._name = v

    def get_type(self):
        return self._type

    def set_type(self, v):
        self._type = v

    def get_set_identifier(self):
        return self._set_identifier

    def set_set_identifier(self, v):
        self._set_identifier = v

    def get_weight(self):
        return self._weight

    def set_weight(self, v):
        self._weight = v

    def get_ttl(self):
        return self._ttl

    def set_ttl(self, v):
        self._ttl = v

    def get_resource_records(self):
        return self._resource_records

    def set_resource_records(self, v):
        self._resource_records = list(v) if v is not None else None

    def get_alias_target(self):
        return self._alias_target

    def set_alias_target(self, v):
        self._alias_target = v

    def get_health_check_id(self):
        return self._health_check_id

    def set_health_check_id(self, v):
        self._health_check_id = v

    def __str__(self):
        fields = [("Name", self._name), ("Type", self._type), ("SetIdentifier", self._set_identifier),
                  ("Weight", self._weight), ("TTL", self._ttl),
                  ("ResourceRecords", None if self._resource_records is None
                   else "[" + ", ".join(str(r) for r in self._resource_records) + "]"),
                  ("AliasTarget", self._alias_target), ("HealthCheckId", self._health_check_id)]
        return "{" + ",".join("%s: %s" % (k, _jstr(v)) for k, v in fields if v is not None) + "}"

    __repr__ = __str__


__all__ = ["ResourceRecord", "ResourceRecordSet", "AliasTarget"]
