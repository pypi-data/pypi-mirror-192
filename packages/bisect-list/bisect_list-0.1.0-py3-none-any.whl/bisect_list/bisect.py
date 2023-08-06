from typing import Callable, TypeVar

from bisect_list.functional import flatten, split_list
from bisect_list.remove_unrelated import remove_unrelated_items

T = TypeVar("T")


class NothingToBisectError(Exception):
    pass


def bisect(values: list[T], test: Callable[[list[T]], bool], *, _skip_initial_test: bool = False) -> list[T]:
    def test_chunks(chunks: list[list[T]]):
        return test(flatten(chunks))

    if not _skip_initial_test:
        if not test(values):
            raise NothingToBisectError(
                f"Nothing to bisect, test function does not return True with initial values: {repr(test)}"
            )

    bisecting: list[list[T] | KnownBad[T]] = [values]

    while True:
        # nothing to split, we done
        if len(bisecting) == 0:
            break

        # nothing left to split! we done!
        if all(len(x) == 1 for x in bisecting):
            break

        # split remaining chunks
        bisecting = [x for xs in bisecting for x in ([xs] if isinstance(xs, KnownBad) else split_list(xs))]

        # remove any chunks that do not affect the result
        bisecting = remove_unrelated_items(bisecting, test=test_chunks, skip=skip_known_bad)

        # mark any chunks that are known to be bad
        bisecting = [KnownBad(x) if len(x) == 1 else x for x in bisecting]

    bad_values = flatten(bisecting)

    return bad_values


def skip_known_bad(x):
    """Skip testing known bad values"""
    return isinstance(x, KnownBad)


class KnownBad(list[T]):
    pass
