import os
import pickle


class FileCache:
    def __init__(self, cache_dir):
        self._cache_dir = cache_dir
        self._cached_keys = set()
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        for cached_pickle in os.listdir(cache_dir):
            key, ext = os.path.splitext(cached_pickle)
            if ext != '.pkl': continue
            self._cached_keys.add(int(key))

    def __setitem__(self, key, value):
        cache_fn = self.cache_fn(key)
        with open(cache_fn, 'wb') as f:
            pickle.dump(value, f)
        self._cached_keys.add(key)

    def __getitem__(self, key):
        cache_fn = self.cache_fn(key)
        try:
            with open(cache_fn, 'rb') as f:
                return pickle.load(f)
        except IOError:
            raise KeyError(key)

    def __len__(self):
        return len(self._cached_keys)

    def __contains__(self, key):
        return key in self._cached_keys

    def clear(self):
        self._cached_keys = set()
        for cached_pickle in os.listdir(self._cache_dir):
            os.unlink(os.path.join(self._cache_dir, cached_pickle))

    def cache_fn(self, key):
        return os.path.join(self._cache_dir, str(key) + '.pkl')
