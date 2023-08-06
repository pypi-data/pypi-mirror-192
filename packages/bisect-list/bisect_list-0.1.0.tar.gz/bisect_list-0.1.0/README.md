# bisect-list

Find bad values in a list, logarithmically (FAST!)!

![](animation.gif)

# install

```shell
poetry add bisect-list
```

# usage

## bisect_exception(values, func)

Logarithmically removes items that don't trigger an exception.

Useful for finding the minimal list of items that triggers an excetpion.

```python
from unittest.mock import MagicMock

from bisect_list import bisect_exception

def error_3705_and_7399(values):
    if 3705 in values and 7399 in values:
        raise Exception(f"Never mix 2 with 5!")

mock_func = MagicMock(side_effect=error_3705_and_7399)

values = list(range(10_000))
result = bisect_exception(values, mock_func)
assert result == [3705, 7399]

assert mock_func.call_count == 53
```

---

## bisect_same_exception(values, func)

Same as `bisect_exception`, except makes sure the type of the exception is the same as when calling `func(values)` before starting the bisection.

```python
from bisect_list import bisect_same_exception

class SpecialException(Exception):
    pass

def error_2_and_5(values):
    if 2 in values and 5 in values:
        raise SpecialException(f"Never mix 2 with 5!")
    raise Exception("different exception")

values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
result = bisect_same_exception(values, error_2_and_5)
assert result == [2, 5]
```

---

## biest(values, test)

```python
from bisect_list import bisect

result = bisect(
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    test=lambda xs: 2 in xs and 8 in xs
)
assert result == [2, 8]
```

# license

MIT
