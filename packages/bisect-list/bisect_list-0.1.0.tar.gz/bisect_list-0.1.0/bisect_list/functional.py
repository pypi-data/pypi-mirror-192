import itertools
from math import ceil
from typing import Iterator, TypeVar

T = TypeVar("T")


def flatten(values: list[list[T]]) -> list[T]:
    return [x for xs in values for x in xs]


def split_list(values: list[T]) -> list[list[T]]:
    if len(values) == 0:
        return []
    if len(values) == 1:
        return [[values[0]]]
    middle = int(ceil(len(values) / 2))
    return [values[:middle], values[middle:]]


def combinations(values: list[T], r: int) -> Iterator[tuple[T]]:
    return itertools.combinations(values, r)


def all_combinations(values: list[T]) -> Iterator[tuple[T]]:
    for r in range(len(values) + 1):
        yield from combinations(values, r)
