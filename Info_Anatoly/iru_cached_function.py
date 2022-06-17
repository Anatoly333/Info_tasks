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
    dict = OrderedDict()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        new_str = ''
        if len(args) > 0:
            for i in range(len(args)):
                new_str += str(args[i]) + ', '

        new_string = ''
        if len(kwargs.items()) > 0:
            for key, value in kwargs.items():
                new_string += str(key) + '=' + str(value) + ', '
        if new_string + new_str in dict.keys():
            return dict[new_str + new_string]
        answer = func(*args, **kwargs)
        dict.update({new_str + new_string: answer})
        return answer
    return wrapper
