import pytest

class DummyHost:
    def __init__(self, hostname):
        self.hostname = hostname

    def get_hostname(self):
        return self.hostname

class TestShardSupplier:
    def __init__(self, shards, current_shard):
        self.shards = shards
        self.current_shard = current_shard

    def get_queue_shards(self):
        return self.shards

    def get_current_shard(self):
        return self.current_shard

    def get_shard_for_host(self, host):
        # Return host's hostname for test
        return host.get_hostname()

def test_shard_supplier_interface():
    shards = {"alpha", "beta"}
    supplier = TestShardSupplier(shards, "beta")
    assert supplier.get_queue_shards() == shards
    assert supplier.get_current_shard() == "beta"
    host = DummyHost("hostY")
    assert supplier.get_shard_for_host(host) == "hostY"

def test_shard_supplier_empty_set():
    supplier = TestShardSupplier(set(), None)
    assert set(supplier.get_queue_shards()) == set()
    assert supplier.get_current_shard() is None