import bisect
from functools import wraps
from typing import Any, Callable, TypeVar

from bisect_list.bisect import NothingToBisectError, bisect

T = TypeVar("T")


def bisect_exception(values: list[T], func: Callable[[list[T]], Any]) -> list[T]:
    try:
        func(values)
    except Exception as e:
        pass
    else:
        raise NothingToBisectError(
            f"Nothing to bisect, function does not raise exception with initial values: {repr(func)}"
        )

    test = test_raised_exception(func)
    bad_values = bisect(values, test, _skip_initial_test=True)
    return bad_values


def bisect_same_exception(values: list[T], func: Callable[[list[T]], Any]) -> list[T]:
    try:
        func(values)
    except Exception as e:
        match_exception_type = type(e)
    else:
        raise NothingToBisectError(
            f"Nothing to bisect, function does not raise exception with initial values: {repr(func)}"
        )

    @wraps(func)
    def test(test_values):
        try:
            func(test_values)
            return False
        except Exception as e:
            if type(e) == match_exception_type:
                return True
            return False

    bad_values = bisect(values, test, _skip_initial_test=True)
    return bad_values


def test_raised_exception(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
            return False
        except Exception as e:
            return True

    return wrapper
