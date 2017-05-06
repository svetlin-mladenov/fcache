from fcache.hashing import stable_hash
from fcache.file_cache import FileCache

import atexit
import logging

logger = logging.getLogger('fcache')

GLOBAL_CACHE = FileCache('.fcache')

def get_global_cache():
    global GLOBAL_CACHE
    return GLOBAL_CACHE

def get_func_fullname(f, bounded_obj):
    f_name = getattr(f, '__module__', '') + '.'
    if bounded_obj is not None:
        f_name += bounded_obj.__class__.__name__ + '.'
    return f_name + getattr(f, '__name__', 'UNKNOWN')


def fcache(f):
    cache = get_global_cache()
    def decorated(*args, **kwargs):
        if f.__closure__:
            f_closure_values = tuple(map(lambda c: c.cell_contents, f.__closure__))
        else:
            f_closure_values = None
        bounded_obj = getattr(f, '__self__', None)
        call_hash = stable_hash((f, args, kwargs, f_closure_values, bounded_obj))
        f_name = get_func_fullname(f, bounded_obj)
        if call_hash in cache:
            logger.info('Cache Hit for %s', f_name)
            return cache[call_hash]
        else:
            logger.info('Cache Miss for %s', f_name)
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
