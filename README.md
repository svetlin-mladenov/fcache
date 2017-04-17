# fcache
fcache caches the result of function calls to memory or disk. When the same function is called with the same arguments the cached result is returned instead of recomputing it. This behavior is ideal for caching results of long running, computationally intensive functions. fcache has been designed for data heavy tasks and works well with `numpy arrays`, `panda dataframes` and inside `ipython` notebooks.


## Features

 * Easy to use API consisting of just a single decorator. No need to manually create temporary directory or provide custom hash functions.
 * Works with (almost) any python object including lambdas, dicts, numpy arrays and panda dataframes.
 * Cached results are persisted between runs of the python interpreter. `fcache` is NOT affected by changes in [PYTHONHASHSEED](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONHASHSEED).
 * Results are cached not just based on the input arguments but also on the function itself.
 * Controll over just how much is being cached. (WIP)
 * Support of hybrid mode of operation where part of the results are cached in-memory and the rest on disk.


## Installation

    pip3 install git+https://github.com/svetlin-mladenov/fcache.git

Please note that `fcache` requires python 3.


## Getting Started


Just import `fcache` and decorate all slow functions with it. Here is the basic usage:

```python
from fcache import fcache

@fcache
def slow_computation(data):
	....
```

Here is another quick example:

```python
from fcache import fcache

@fcache
def fib(n):
	if n < 2: return n
	return fib(n-1) + fib(n-2)
```

## Cavities

 * `fcache` assumes that decorated functions are [pure](https://en.wikipedia.org/wiki/Pure_function). Needless to say that this assumtion does not hold for most functions. In order to compensate `fcache` looks not just at the function but also at its closure and global variables. This can also fail in certain circumstances leading to function calls that are not cached but should be or vice versa. If you are affected by such a problem please open an issue.
 * `fcache` hashes the decorated fucntion but not its dependancies (the functions it calls and the function they call and so on). This means that if any of these dependancies changes the cache will not be invalidated, leading to stale and wrong values being returned by `fcache` decorated functions. If you have any ideas how to handle these cases please open an issue.
 * For the time being it works only with `python 3`

