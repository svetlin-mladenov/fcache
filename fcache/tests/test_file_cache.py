from fcache.file_cache import FileCache


def test_caching_values(tmpdir):
    cache = FileCache(str(tmpdir))
    kvs = [(1, 1), (2, 20), (3, 300)]
    for k, v in kvs:
        cache[k] = v
    for k, v in kvs:
        assert k in cache
        assert cache[k] == v
    assert len(cache) == 3

    # test that values are preserved between runs
    del cache
    cache = FileCache(str(tmpdir))
    for k, v in kvs:
        assert k in cache
        assert cache[k] == v
    assert len(cache) == 3


def test_cache_clearing(tmpdir):
    cache = FileCache(str(tmpdir))
    kvs = [(1, 1), (2, 20), (3, 300)]
    for k, v in kvs:
        cache[k] = v
    assert len(cache) == 3
    cache.clear()
    assert len(cache) == 0


def test_cache_limit(tmpdir):
    record_size = 512
    cache = FileCache(str(tmpdir), capacity=int(2.5*record_size))
    cache[0] = bytes(record_size)
    cache[1] = bytes(record_size)
    cache[2] = bytes(record_size)
    assert 0 not in cache  # 0 is the LRU
    assert 1 in cache
    assert 2 in cache

    assert cache[1] is not None  # make 2 the LRU
    cache[3] = bytes(record_size)
    assert 0 not in cache
    assert 2 not in cache
    assert 1 in cache
    assert 3 in cache


def test_cache_limit_restore_from_disk(tmpdir):
    record_size = 512
    cache = FileCache(str(tmpdir), capacity=int(2.5*record_size))
    cache[0] = bytes(record_size)
    cache[1] = bytes(record_size)
    cache[2] = bytes(record_size)

    del cache
    cache = FileCache(str(tmpdir), capacity=int(2.5*record_size))
    assert 0 not in cache
    assert 1 in cache
    assert 2 in cache

    cache[3] = bytes(record_size)
    assert 1 not in cache
