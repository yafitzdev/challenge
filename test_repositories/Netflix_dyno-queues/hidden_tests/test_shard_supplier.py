import pytest

class DummyHost:
    def __init__(self, hostname, rack):
        self.hostname = hostname
        self.rack = rack

    def get_rack(self):
        return self.rack

class TestShardSupplier:
    def __init__(self, shards, current_shard):
        self.shards = shards
        self.current_shard = current_shard

    def get_queue_shards(self):
        return self.shards

    def get_current_shard(self):
        return self.current_shard

    def get_shard_for_host(self, host):
        # mimic rack name for test
        return host.get_rack()

def test_shard_supplier_interface():
    shards = {"one", "two"}
    supplier = TestShardSupplier(shards, "one")
    assert supplier.get_queue_shards() == shards
    assert supplier.get_current_shard() == "one"
    host = DummyHost("host", "rck")
    assert supplier.get_shard_for_host(host) == "rck"

def test_shard_supplier_empty_set():
    supplier = TestShardSupplier(set(), None)
    assert set(supplier.get_queue_shards()) == set()
    assert supplier.get_current_shard() is None