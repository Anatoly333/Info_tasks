"""
This module contains run_verbosely function,
which logs parameters of another function call.
"""
import functools
from collections import OrderedDict


def cached_function(func):
    """
    Print name of called func function,
    print its args, kwargs and return value.
    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        string_args, string_kwargs = creating_key(*args, **kwargs)
        if string_kwargs + string_args in cache:
            return cache[string_args + string_kwargs]
        answer = func(*args, **kwargs)
        cache[string_args + string_kwargs] = answer
        return answer
    return wrapper

def creating_key(*args, **kwargs):
    '''
    Creating key
    '''
    string_args = ''
    if len(args) > 0:
        for i in args:
            string_args += str(i) + ', '
    string_kwargs = ''
    if len(kwargs.items()) > 0:
        for key, value in kwargs.items():
            string_kwargs += str(key) + '=' + str(value) + ', '
    return string_args, string_kwargs

def lru_cached_function(cache_size=10):
    """
    Print name of called func function,
    print its args, kwargs and return value.
    """
    cache = OrderedDict()

    def get_function(func):
        if not isinstance(cache_size, int):
            raise TypeError('cache_size must be int not ' + type(cache_size).__name__)
        if cache_size <= 0:
            raise TypeError('cache_size must be positive')

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = []
            if len(args) > 0:
                for i in args:
                    cache_key.append(str(i))

            if len(kwargs.items()) > 0:
                for key, value in kwargs.items():
                    cache_key.append(str(key) + str(value))
            cache_key.sort()
            cache_key = tuple(cache_key)
            if cache.get(cache_key is not None):
                cache.move_to_end(cache_key)
                return cache[cache_key]
            answer = func(*args, **kwargs)
            if len(cache) >= cache_size:
                cache.pop(list(cache.keys())[0])
            cache.update({cache_key: answer})
            return answer
        return wrapper
    return get_function
