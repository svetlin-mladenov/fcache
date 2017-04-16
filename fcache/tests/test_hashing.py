import pytest
import sys
import subprocess
import os

from fcache.hashing import stable_hash


def get_hash_command(repr_):
    return 'from fcache.hashing import stable_hash; print(stable_hash(%s))' % repr_


def get_hash(repr_):
    # copy pasted from https://hg.python.org/cpython/file/5e8fa1b13516/Lib/test/test_hash.py#l145
    env = os.environ
    cmd_line = [sys.executable, '-c', get_hash_command(repr_)]
    p = subprocess.Popen(cmd_line, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             env=env)
    out, err = p.communicate()
    return int(out.strip())


@pytest.mark.parametrize('object_to_hash', ['string', (('key1', 1), ('key2', 2)),
                                            {'key1': 10, 'key2': 20}, {1, 50, 10, 20},
                                            5, ('str', 10), [2, 3, 'xv']])
def test_cache_stability(object_to_hash):
    expected_hash = stable_hash(object_to_hash)
    for _ in range(3):
        another_hash = get_hash(repr(object_to_hash))
        assert expected_hash == another_hash
