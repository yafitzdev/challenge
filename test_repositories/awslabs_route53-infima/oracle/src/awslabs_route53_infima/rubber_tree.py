from src.awslabs_route53_model import AliasTarget, ResourceRecordSet

from .lattice import Lattice
from .util.answer_set import AnswerSet
from .util.iterable_sub_list_generator import IterableSubListGenerator


class RubberTree:

    @staticmethod
    def vulcanize(hosted_zone_id, name, type, ttl, lattice_or_records, records_per_record_set):
        if isinstance(lattice_or_records, Lattice):
            return RubberTree._vulcanize_lattice(hosted_zone_id, name, type, ttl,
                                                 lattice_or_records, records_per_record_set)
        return RubberTree._vulcanize_records(hosted_zone_id, name, type, ttl,
                                             lattice_or_records, records_per_record_set)

    @staticmethod
    def _vulcanize_lattice(hosted_zone_id, name, type, ttl, lattice, records_per_record_set):
        if len(lattice.get_all_coordinates()) == 1:
            return RubberTree._vulcanize_records(hosted_zone_id, name, type, ttl,
                                                 lattice.get_all_endpoints(), records_per_record_set)

        coordinates = sorted(lattice.get_all_coordinates())
        coordinates.sort(key=len)  # (unused further, as in the Java source)

        hcrr = []
        for coordinate in sorted(lattice.get_all_coordinates()):
            to_splice = lattice.get_endpoints_for_sector(list(coordinate))
            new_size = len(hcrr) + len(to_splice)
            spacing = float(new_size // len(to_splice))
            i = 0
            for endpoint in to_splice:
                hcrr.insert(int(i * spacing), endpoint)
                i += 1

        vulcanized = RubberTree._vulcanize_records(hosted_zone_id, name, type, ttl, hcrr,
                                                   records_per_record_set)

        if len(lattice.get_all_coordinates()) > 1:
            secondary_name = "secondary." + name
            for rr in vulcanized:
                if rr.get_weight() == 0:
                    rr.set_name(secondary_name)
                    rr.set_weight(1)

            for dimension in lattice.get_dimension_names():
                for value in list(lattice.get_dimension_values(dimension)):
                    prefix = dimension[:min(len(dimension), 30)] + "-" + value[:min(len(value), 30)]
                    sub_tree_name = prefix + "." + secondary_name
                    target = AliasTarget()
                    target.set_dns_name(sub_tree_name)
                    target.set_evaluate_target_health(True)
                    target.set_hosted_zone_id(hosted_zone_id)
                    rr = ResourceRecordSet()
                    rr.set_name(secondary_name)
                    rr.set_weight(0)
                    rr.set_type(type)
                    rr.set_alias_target(target)
                    rr.set_set_identifier(prefix)
                    vulcanized.extend(RubberTree._vulcanize_records(
                        hosted_zone_id, sub_tree_name, type, ttl,
                        lattice.simulate_failure(dimension, value).get_all_endpoints(),
                        records_per_record_set))
                    vulcanized.append(rr)

            target = AliasTarget()
            target.set_dns_name(secondary_name)
            target.set_evaluate_target_health(True)
            target.set_hosted_zone_id(hosted_zone_id)
            rr = ResourceRecordSet()
            rr.set_name(name)
            rr.set_weight(0)
            rr.set_type(type)
            rr.set_alias_target(target)
            rr.set_set_identifier("secondary for " + name)
            vulcanized.append(rr)
        return vulcanized

    @staticmethod
    def _vulcanize_records(hosted_zone_id, name, type, ttl, records, records_per_record_set):
        rrs = []
        hcrr = list(records)
        if records_per_record_set > 8:
            raise ValueError("Rubber Tree supports 8 or fewer records or record set")
        if len(hcrr) > records_per_record_set:
            original_count = len(hcrr)
            hcrr.extend(hcrr[0:records_per_record_set - 1])
            for i in range(original_count):
                answer = AnswerSet()
                answer.add_all(hcrr[i:i + records_per_record_set])
                rrs.extend(answer.to_resource_record_sets(hosted_zone_id, name, type, ttl))
            return rrs

        answer = AnswerSet()
        answer.add_all(hcrr)
        rrs.extend(answer.to_resource_record_sets(hosted_zone_id, name, type, ttl))
        for fragment in IterableSubListGenerator(records, records_per_record_set - 1):
            answer = AnswerSet()
            answer.add_all(fragment)
            rrs.extend(answer.to_resource_record_sets(hosted_zone_id, name, type, ttl))
            rrs[-1].set_weight(0)
        return rrs
