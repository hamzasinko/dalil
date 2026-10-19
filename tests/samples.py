"""Sample functions shared by the unit and edge test suites.

These plain, un-decorated functions are used both as fixtures (see
``tests/conftest.py``) and directly by the Hypothesis property tests,
which cannot take pytest fixtures as ``@given`` parameters.
"""

from collections.abc import Callable


def fibonacci(n: int) -> int:
    """Return the n-th Fibonacci number (naive recursion)."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def bubble_sort(items: list[int]) -> list[int]:
    """Return a sorted copy of ``items`` using bubble sort."""
    result = list(items)
    n = len(result)
    for i in range(n):
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
    return result


def binary_search(items: list[int], target: int) -> int:
    """Return the index of ``target`` in sorted ``items``, else ``-1``."""
    low, high = 0, len(items) - 1
    while low <= high:
        middle = (low + high) // 2
        if items[middle] == target:
            return middle
        if items[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


def linear_sum(n: int) -> int:
    """Return the sum of ``range(n)`` (single loop, O(n))."""
    total = 0
    for i in range(n):
        total += i
    return total


SAMPLE_FUNCTIONS: dict[str, Callable[..., object]] = {
    "fibonacci": fibonacci,
    "bubble_sort": bubble_sort,
    "binary_search": binary_search,
    "linear_sum": linear_sum,
}
"""Named access to every sample function."""
