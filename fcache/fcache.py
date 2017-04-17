from fcache.hashing import stable_hash
from fcache.file_cache import FileCache

import atexit


GLOBAL_CACHE = FileCache('.fcache')

def get_global_cache():
    global GLOBAL_CACHE
    return GLOBAL_CACHE

def fcache(f):
    cache = get_global_cache()
    def decorated(*args, **kwargs):
        if f.__closure__:
            f_closure_values = tuple(map(lambda c: c.cell_contents, f.__closure__))
        else:
            f_closure_values = None
        bounded_obj = getattr(f, '__self__', None)
        call_hash = stable_hash((f, args, kwargs, f_closure_values, bounded_obj))
        if call_hash in cache:
            return cache[call_hash]
        else:
            ret_val = f(*args, **kwargs)
            cache[call_hash] = ret_val
            return ret_val
    return decorated
fcache.clear_at_exit = False

@atexit.register
def maybe_clear_at_exit():
    if fcache.clear_at_exit:
        global GLOBAL_CACHE
        GLOBAL_CACHE.clear()
