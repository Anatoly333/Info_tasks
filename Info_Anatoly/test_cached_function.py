"""
Tests for lru_cached_function decorator.
"""

import textwrap

import pytest

from cache_decorators import cached_function
from common import get_page_name, print_and_return_arg


@pytest.mark.parametrize(
    'func',
    [
        get_page_name,
        print_and_return_arg,
    ]
)
# pylint: disable=C0116
def test_func_saves_its_properties(func):
    cached_func = cached_function(func)
    assert cached_func.__name__ == func.__name__
    assert cached_func.__annotations__ == func.__annotations__
    assert cached_func.__qualname__ == func.__qualname__
    assert cached_func.__doc__ == func.__doc__
    assert cached_func.__module__ == func.__module__


def test_get_page_name(capsys):  # pylint: disable=C0116
    cached_get_page_name = cached_function(get_page_name)
    for _ in range(1000):
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


def test_print_and_return_x(capsys):  # pylint: disable=C0116
    cached_print_and_return_x = cached_function(print_and_return_arg)
    assert cached_print_and_return_x.__name__ == print_and_return_arg.__name__
    assert cached_print_and_return_x.__annotations__ == print_and_return_arg.__annotations__
    assert cached_print_and_return_x.__qualname__ == print_and_return_arg.__qualname__
    assert cached_print_and_return_x.__doc__ == print_and_return_arg.__doc__
    assert cached_print_and_return_x.__module__ == print_and_return_arg.__module__
    for _ in range(1000):
        assert cached_print_and_return_x(2) == 2
        assert cached_print_and_return_x(1.5) == 1.5
        assert cached_print_and_return_x(1.5-2.5j) == 1.5-2.5j
        assert cached_print_and_return_x(True) is True
        assert cached_print_and_return_x('испанская инквизиция') == 'испанская инквизиция'
        assert cached_print_and_return_x((5, 0, 0, 6)) == (5, 0, 0, 6)
        assert cached_print_and_return_x(range(9)) == range(9)
        assert cached_print_and_return_x(frozenset({7, 7, 7, 7})) == frozenset({7, 7, 7, 7})
        assert cached_print_and_return_x(b'\x00\x10') == b'\x00\x10'
    captured_out = capsys.readouterr()
    assert captured_out.out == textwrap.dedent("""\
        2
        1.5
        (1.5-2.5j)
        True
        испанская инквизиция
        (5, 0, 0, 6)
        range(0, 9)
        frozenset({7})
        b'\\x00\\x10'
    """)
