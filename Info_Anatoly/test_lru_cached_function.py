"""
Tests for lru_cached_function decorator.
"""

import textwrap

import pytest

from cache_decorators import lru_cached_function
from common import get_page_name, get_sum_len_of_args_and_kwargs, print_and_return_arg


@pytest.mark.parametrize(
    'func',
    [
        get_page_name,
        get_sum_len_of_args_and_kwargs,
        print_and_return_arg,
     ]
)
# pylint: disable=C0116
def test_clear_wrapper(func):
    cached_func = lru_cached_function(cache_size=10)(func)
    assert cached_func.__name__ == func.__name__
    assert cached_func.__annotations__ == func.__annotations__
    assert cached_func.__qualname__ == func.__qualname__
    assert cached_func.__doc__ == func.__doc__
    assert cached_func.__module__ == func.__module__


def test_get_page_name_right_cache_size(capsys):  # pylint: disable=C0116
    cached_get_page_name = lru_cached_function(cache_size=4)(get_page_name)
    for _ in range(100):
        assert cached_get_page_name(74) == 'Фонетика русских диалектов (74)'
        assert cached_get_page_name(75) == 'Фонетика русских диалектов (75)'
        assert cached_get_page_name(76) == 'Фонетика русских диалектов (76)'
        assert cached_get_page_name(76) == 'Фонетика русских диалектов (76)'
        assert cached_get_page_name(77) == 'Фонетика русских диалектов (77)'
    captured_out = capsys.readouterr()
    assert captured_out.out == textwrap.dedent("""\
        Got content for page 74!
        Got content for page 75!
        Got content for page 76!
        Got content for page 77!
    """)


def test_get_page_name_short_cache_size(capsys):  # pylint: disable=C0116
    cached_get_page_name = lru_cached_function(cache_size=3)(get_page_name)
    for _ in range(2):
        assert cached_get_page_name(74) == 'Фонетика русских диалектов (74)'
        assert cached_get_page_name(75) == 'Фонетика русских диалектов (75)'
        assert cached_get_page_name(76) == 'Фонетика русских диалектов (76)'
        assert cached_get_page_name(76) == 'Фонетика русских диалектов (76)'
        assert cached_get_page_name(77) == 'Фонетика русских диалектов (77)'
    captured_out = capsys.readouterr()
    assert captured_out.out == textwrap.dedent("""\
        Got content for page 74!
        Got content for page 75!
        Got content for page 76!
        Got content for page 77!
        Got content for page 74!
        Got content for page 75!
        Got content for page 76!
        Got content for page 77!
    """)


def test_wrong_cache_size():  # pylint: disable=C0116
    with pytest.raises(TypeError, match='cache_size must be int not str'):
        _ = lru_cached_function(cache_size='0')(get_page_name)
    with pytest.raises(TypeError, match='cache_size must be int not float'):
        _ = lru_cached_function(cache_size=0.0)(get_page_name)
    with pytest.raises(TypeError, match='cache_size must be int not set'):
        _ = lru_cached_function(cache_size={0, 1, 2, 3})(get_page_name)
    with pytest.raises(TypeError, match='cache_size must be positive'):
        _ = lru_cached_function(cache_size=0)(get_page_name)
    with pytest.raises(TypeError, match='cache_size must be positive'):
        _ = lru_cached_function(cache_size=-5)(get_page_name)


def test_get_sum_len_of_args_and_kwargs(capsys):  # pylint: disable=C0116
    cached_get_sum_len_of_args_and_kwargs = lru_cached_function(
        cache_size=1
    )(get_sum_len_of_args_and_kwargs)
    for _ in range(100):
        assert cached_get_sum_len_of_args_and_kwargs(2, 3.5, 4.5+5.5j, a="6.5", b=(7.5,)) == 5
        assert cached_get_sum_len_of_args_and_kwargs(2, 3.5, 4.5+5.5j, b=(7.5,), a="6.5") == 5
    captured_out = capsys.readouterr()
    assert captured_out.out == textwrap.dedent("""\
        args are: (2, 3.5, (4.5+5.5j)), kwargs are: {'a': '6.5', 'b': (7.5,)}
    """)
