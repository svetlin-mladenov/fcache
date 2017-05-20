import hashlib
import pickle
import io


class StablePickler(pickle.Pickler):
    def persistent_id(self, obj):
        if hasattr(obj, '__code__'):
            return obj.__code__.co_code
        elif isinstance(obj, dict):
            return sorted(obj.items())
        elif isinstance(obj, set):
            return sorted(obj)
        return None


def stable_hash(obj):
    file = io.BytesIO()
    StablePickler(file).dump(obj)
    dumps = file.getvalue()
    hasher = hashlib.sha1()
    hasher.update(dumps)
    return int.from_bytes(hasher.digest(), 'little')
