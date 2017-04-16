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
