import textwrap

import pytest

from run_verbosely import run_verbosely


def do_nothing():
    pass


DO_NOTHING_OUT = textwrap.dedent("""\
    Calling do_nothing() function
    Args are: 
    Kwargs are: 
    Return value is: None
""")


def return_some_str(a, b, c, *, d, e, f):
    return "some_str"


RETURN_SOME_STR_OUT = textwrap.dedent("""\
    Calling return_some_str() function
    Args are: 1, 2, 3
    Kwargs are: d=5, e=6, f=hey
    Return value is: some_str
""")


def print_42_twice():
    print(42)
    print(42)


PRINT_42_TWICE_OUT = textwrap.dedent("""\
    Calling print_42_twice() function
    Args are: 
    Kwargs are: 
    42
    42
    Return value is: None
""")


def print_and_return(int0, int1, *, some_string):
    print(some_string * (int0 + int1))
    return some_string * (int0 + int1 + 1)


PRINT_AND_RETURN_OUT = textwrap.dedent("""\
    Calling print_and_return() function
    Args are: 1, 3
    Kwargs are: some_string=abc
    abcabcabcabc
    Return value is: abcabcabcabcabc
""")


TEST_DATA = [
    (print_42_twice, PRINT_42_TWICE_OUT, (), {}, None),
    (
        return_some_str, RETURN_SOME_STR_OUT,
        (1, 2, 3), {'d': 5, 'e': 6, 'f': 'hey'},
        'some_str'
    ),
    (do_nothing, DO_NOTHING_OUT, (), {}, None),
    (print_and_return, PRINT_AND_RETURN_OUT, (1, 3), {'some_string': 'abc'}, 'abcabcabcabcabc')
]


@pytest.mark.parametrize(
    argnames='func, captured_out, args, kwargs, return_value',
    argvalues=TEST_DATA,
    ids=[case[0].__name__ for case in TEST_DATA]
)
def test_run_verbosely(capsys, func, captured_out, args, kwargs, return_value):
    func = run_verbosely(func)
    assert func(*args, **kwargs) == return_value
    captured = capsys.readouterr()
    assert captured.out == captured_out


@pytest.mark.parametrize(
    argnames='func, captured_out',
    argvalues=[
        (do_nothing, DO_NOTHING_OUT * 3),
    ],
    ids=['do_nothing'])
def test_run_verbosely_three_times(capsys, func, captured_out):
    func = run_verbosely(func)
    func()
    func()
    func()
    captured = capsys.readouterr()
    assert captured.out == captured_out
