from typing import Callable, TypeVar

T = TypeVar("T")


def remove_unrelated_items(
    chunks: list[T], *, test: Callable[[list[T]], bool], skip: Callable[[T], bool] | None = None
) -> list[T]:
    """
    Removes items that have no affect on `test` returning true.
    """
    included_chunks = []
    for i, chunk in enumerate(chunks):
        remaining_chunks = chunks[i + 1 :]
        with_chunk_removed = [*included_chunks, *remaining_chunks]
        if skip is not None and skip(chunk):
            # Marked chunk to be included, no need to test removing it
            included_chunks.append(chunk)
        else:
            if test(with_chunk_removed):
                # Remove chunk didn't make test fail, so we can remove it
                pass
            else:
                included_chunks.append(chunk)
    return included_chunks
