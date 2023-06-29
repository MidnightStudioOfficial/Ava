import cachetools
import CacheToolsUtils as ctu

from smart_cache import smart_cache

ct_base = cachetools.TTLCache(maxsize=100, ttl=600)
foo_cache = ctu.PrefixedCache(ct_base, "foo.")
bla_cache = ctu.PrefixedCache(ct_base, "bla.")

@cachetools.cached(cache=foo_cache)
def foo(n):
    for i in range(10):
        n += 4.65
        n = n*5
    return n

@smart_cache
def foo3(n):
    for i in range(10):
        n += 4.65
        n = n*5
    return n


def foo2(n):
    for i in range(10):
        n += 4.65
        n = n*5
    return n

@cachetools.cached(cache=bla_cache)
def bla(n):
    return n

def not_time():
    n2 = 0
    while n2 != 10:
        foo(n2)
        n2 += 1
def is_time():
    n2 = 0
    while n2 != 10:
        foo2(n2)
        n2 += 1

def not_time2():
    n2 = 0
    while n2 != 10:
        foo3(n2)
        n2 += 1

import timeit
print(timeit.timeit("not_time()", setup="from __main__ import not_time", number=10))
print(timeit.timeit("is_time()", setup="from __main__ import is_time", number=10))
print(timeit.timeit("not_time2()", setup="from __main__ import not_time2", number=10))
import jsonpickle
frozen = jsonpickle.encode(ct_base)
print(frozen)
