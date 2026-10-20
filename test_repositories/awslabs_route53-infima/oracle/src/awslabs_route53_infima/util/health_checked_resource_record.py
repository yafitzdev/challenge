from .comparable_resource_record import ComparableResourceRecord


class HealthCheckedResourceRecord(ComparableResourceRecord):
    def __init__(self, healthcheck_ids, record_data):
        super().__init__(record_data)
        if isinstance(healthcheck_ids, (list, tuple)):
            self._healthcheck_ids = healthcheck_ids
        else:
            self._healthcheck_ids = [healthcheck_ids]

    def get_healthcheck_ids(self):
        return self._healthcheck_ids
