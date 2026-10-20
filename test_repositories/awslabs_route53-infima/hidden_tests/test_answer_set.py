import pytest

# Import required classes from implementation
from src.awslabs_route53_infima.util import AnswerSet, ComparableResourceRecord, HealthCheckedResourceRecord
from src.awslabs_route53_model import ResourceRecordSet

def test_ordering():
    answer = AnswerSet()
    answer.add(ComparableResourceRecord("3.3.3.3"))
    answer.add(ComparableResourceRecord("2.2.2.2"))
    answer.add(ComparableResourceRecord("1.1.1.1"))

    # Duplicate add should fail (return False)
    assert answer.add(ComparableResourceRecord("1.1.1.1")) is False

    records = [None] * 3
    answer.to_array(records)
    assert records[0].get_value() == "1.1.1.1"
    assert records[1].get_value() == "2.2.2.2"
    assert records[2].get_value() == "3.3.3.3"

def test_simple_rrset():
    answer = AnswerSet()
    answer.add(ComparableResourceRecord("3.3.3.3"))
    answer.add(ComparableResourceRecord("2.2.2.2"))
    answer.add(ComparableResourceRecord("1.1.1.1"))

    rrsets = answer.to_resource_record_sets("Z123", "www.example.com", "A", 60)
    assert len(rrsets) == 1
    rrset = rrsets[0]
    assert rrset.get_ttl() == 60
    assert rrset.get_type() == "A"
    assert rrset.get_name() == "www.example.com"
    assert rrset.get_resource_records()[0].get_value() == "1.1.1.1"
    assert rrset.get_resource_records()[1].get_value() == "2.2.2.2"
    assert rrset.get_resource_records()[2].get_value() == "3.3.3.3"

def test_health_checked_rrset():
    answer = AnswerSet()
    answer.add(HealthCheckedResourceRecord("hcid1", "3.3.3.3"))
    answer.add(HealthCheckedResourceRecord("hcid2", "2.2.2.2"))
    answer.add(HealthCheckedResourceRecord("hcid3", "1.1.1.1"))

    rrsets = answer.to_resource_record_sets("Z123", "www.example.com", "A", 60)
    assert len(rrsets) == 3

    assert rrsets[0].get_ttl() == 60
    assert rrsets[0].get_type() == "A"
    assert rrsets[0].get_resource_records()[0].get_value() == "1.1.1.1"
    assert rrsets[0].get_resource_records()[1].get_value() == "2.2.2.2"
    assert rrsets[0].get_resource_records()[2].get_value() == "3.3.3.3"
    assert rrsets[0].get_health_check_id() == "hcid1"

    # Next rrset is an alias, points to first one
    assert rrsets[1].get_type() == "A"
    assert rrsets[1].get_alias_target().get_dns_name() == rrsets[0].get_name()
    assert rrsets[1].get_alias_target().get_hosted_zone_id() == "Z123"
    assert rrsets[1].get_alias_target().get_evaluate_target_health() is True

    # Final rrset points to second
    assert rrsets[2].get_type() == "A"
    assert rrsets[2].get_alias_target().get_dns_name() == rrsets[1].get_name()
    assert rrsets[2].get_alias_target().get_hosted_zone_id() == "Z123"
    assert rrsets[2].get_alias_target().get_evaluate_target_health() is True

    # Final rrset is entry node
    assert rrsets[2].get_name() == "www.example.com"