"""
This module contains run_verbosely function,
which logs parameters of another function call.
"""


def run_verbosely(func):
    """
    Print name of called func function,
    print its args, kwargs and return value.
    """

    def wrapper(*args, **kwargs):

        print('Calling', func.__name__ + '()', 'function')
        new_str = ''
        if len(args) > 0:
            for i in range(len(args)):
                new_str += str(args[i]) + ', '
            print('Args are:', new_str[0:len(new_str) - 2])
        else:
            print('Args are: ')

        new_string = ''
        if len(kwargs.items()) > 0:
            for key, value in kwargs.items():
                new_string += str(key) + '=' + str(value) + ', '
            print("Kwargs are:", new_string[0:len(new_string) - 2])
        else:
            print("Kwargs are: ")
        answer = func(*args, **kwargs)
        print('Return value is:', answer)
        return answer
    return wrapper
