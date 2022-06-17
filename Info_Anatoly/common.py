"""
Functions for tests for caching decorators.
"""

import typing as tp

from bs4 import BeautifulSoup
import requests

PAGE_URL = 'https://dialect.philol.msu.ru/main.php?page={page_id}'


def get_page_name(page_id: int) -> str:
    """Return topic of page by page_id"""
    response = requests.get(PAGE_URL.format(page_id=page_id))
    response.encoding = response.apparent_encoding
    assert response.status_code == 200, 'Failed to get content!'
    parsed_content = BeautifulSoup(response.text, 'html.parser')
    print(f'Got content for page {page_id}!')
    return parsed_content.find('title').text.strip()


def get_sum_len_of_args_and_kwargs(*args, **kwargs):
    """Print args, then return len of args."""
    print(f'args are: {args}, kwargs are: {kwargs}')
    return len(args) + len(kwargs)


def print_and_return_arg(arg: tp.Any) -> tp.Any:
    """Print arg, then return arg."""
    print(arg)
    return arg
