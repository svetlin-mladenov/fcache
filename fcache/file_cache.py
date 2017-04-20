import os
import pickle


# TODO use slots
class LruItem:
    def __init__(self, prev, next, key):
        self.prev = prev
        self.next = next
        self.key = key

# TODO use slots
class LruList:
    def __init__(self, next):
        self.next = next

class FileCache:
    def __init__(self, cache_dir, capacity=80*1024*1024*1024):
        self._cache_dir = cache_dir
        self._cached_keys = dict()
        self._capacity = capacity
        self._lru_items = LruList(None)  # Dummy item in order to make popping easier
        self._mru_item = self._lru_items
        self._fill = 0
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        disk_files = []
        for cached_pickle in os.listdir(cache_dir):
            key, ext = os.path.splitext(cached_pickle)
            if ext != '.pkl': continue
            key = int(key)
            full_fn = os.path.join(cache_dir, cached_pickle)
            disk_files.append((full_fn, os.stat(full_fn), key))
        for _, stat, key in sorted(disk_files, key=lambda r: r[1].st_atime_ns):
            self._fill += stat.st_size
            self._cached_keys[key] = self.insert_mru(key)

    def __setitem__(self, key, value):
        cache_fn = self.cache_fn(key)
        with open(cache_fn, 'wb') as f:
            pickle.dump(value, f)
            self._fill += f.tell()
        self._cached_keys[key] = self.insert_mru(key)
        while self._fill > self._capacity:
            self.pop_lru()

    def insert_mru(self, key):
        lru_item = LruItem(self._mru_item, None, key)
        self._mru_item.next = lru_item
        self._mru_item = lru_item
        return lru_item

    def __getitem__(self, key):
        lru_item = self._cached_keys[key]
        if lru_item is not self._mru_item:
            lru_item.prev.next = lru_item.next
            if lru_item.next is not None:
                lru_item.next.prev = lru_item.prev
            self._mru_item.next = lru_item
            lru_item.prev = self._mru_item
            lru_item.next = None
            self._mru_item = lru_item
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

    def pop_lru(self):
        lru = self._lru_items.next
        #del self[lru.key]
        del self._cached_keys[lru.key]
        size = os.stat(self.cache_fn(lru.key)).st_size
        os.unlink(self.cache_fn(lru.key))
        lru.prev.next = lru.next
        if lru.next is not None:
            lru.next.prev = lru.prev
        lru.next = None  # no dangling references
        self._fill -= size

    def clear(self):
        self._cached_keys = set()
        for cached_pickle in os.listdir(self._cache_dir):
            os.unlink(os.path.join(self._cache_dir, cached_pickle))

    def cache_fn(self, key):
        return os.path.join(self._cache_dir, str(key) + '.pkl')
