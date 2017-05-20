from fcache import fcache

fcache.clear_at_exit = True


class Num:
    def __init__(self, n):
        self.n = n

    def __eq__(self, other):
        return self.n == other.n

    def __hash__(self):
        return hash(self.n)

    def __iadd__(self, other):
        self.n += other.n
        return self


# Test global function

global_function_call_counter = 0


def global_function(n):
    global global_function_call_counter
    global_function_call_counter += 1
    return n * n


def test_global_function():
    cached = fcache(global_function)
    exp_5 = global_function(5)
    exp_1000 = global_function(1000)
    exp_large = global_function(10000000)
    global global_function_call_counter
    assert global_function_call_counter == 3

    for _ in range(2):
        assert cached(5) == exp_5
        assert cached(1000) == exp_1000
        assert cached(10000000) == exp_large
        assert global_function_call_counter == 6


# Test local function
def test_local_function():
    def loc_func(n):
        loc_func._num_calls_ += 1
        return n * n
    loc_func._num_calls_ = 0
    cached = fcache(loc_func)
    for i in range(5):
        for n in range(5):
            assert cached(n) == loc_func(n)
        assert loc_func._num_calls_ == 5 * (i + 2)


# Test lambda
def test_lambda():
    lamb = lambda x: x  # NOQA
    cached = fcache(lamb)
    for i in range(5):
        for n in range(5):
            f_input = Num(n)
            actual_res = lamb(f_input)
            cached_res = cached(f_input)
            assert actual_res == cached_res
            if i == 0:
                assert f_input is cached_res
            else:
                assert f_input is not cached_res


# Test redifining a function
def test_redefining_a_function():
    @fcache
    def f1(n):
        return n + 1
    for n in range(5):
        return f1(n) == (n + 1)

    @fcache
    def f1(n):
        return n + 2
    for n in range(5):
        return f1(n) == (n + 2)


# Test kwargs
def test_kwargs():
    @fcache
    def fun(n, add=1):
        return n + add

    assert fun(10) == 11
    assert fun(10, add=20) == 30


# Test closure
def test_closure():

    def outer():
        n = Num(0)

        @fcache
        def mut():
            nonlocal n
            n += Num(1)
            return n

        @fcache
        def get():
            return n
        return mut, get
    mut, get = outer()
    assert mut() == Num(1)
    assert get() == Num(1)
    assert mut() == Num(2)
    assert mut() == Num(3)
    get_res = get()
    cached_res = get()
    assert get_res == Num(3)
    assert cached_res == get_res
    assert cached_res is not get_res


# Test class function
class SimpleClass:
    def __init__(self):
        self.n = 0

    def inc(self):
        self.n += 1

    def get(self):
        return self.n


def test_bound_method():
    obj = SimpleClass()
    fun = fcache(obj.get)
    assert fun() == 0
    obj.inc()
    obj.inc()
    assert fun() == 2


# TODO Test well behaived

# Test with numpy and pandas - in a separate file
