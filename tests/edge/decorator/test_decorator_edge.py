"""Edge-case tests for the ``trace`` decorator.

Covers empty / argument-less / return-less functions, recursion,
generators, async functions, lambdas, nested functions, methods,
exception propagation, decorator stacking, repeated and concurrent
calls, and restoration of ``sys.settrace``.
"""

import asyncio
import functools
import sys
from collections.abc import Callable, Iterator
from concurrent.futures import ThreadPoolExecutor
from typing import Any, TypeVar

import pytest

import dalil
from dalil.decorator import TracedFunction
from tests import samples

_R = TypeVar("_R")


def plain_decorator(func: Callable[..., _R]) -> Callable[..., _R]:
    """Return a passthrough decorator used for stacking tests."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> _R:
        return func(*args, **kwargs)

    return wrapper


def test_empty_function() -> None:
    @dalil.trace
    def empty() -> None:
        """Do nothing."""

    assert empty() is None


def test_function_without_return() -> None:
    @dalil.trace
    def side_effect_only(x: int) -> None:
        """Record nothing; implicitly returns ``None``."""
        _ = x * 2

    assert side_effect_only(3) is None


def test_function_without_arguments() -> None:
    @dalil.trace
    def constant() -> int:
        """Return 42."""
        return 42

    assert constant() == 42


def test_function_with_varargs() -> None:
    @dalil.trace
    def total(*args: int) -> int:
        """Return the sum of ``args``."""
        return sum(args)

    assert total(1, 2, 3) == 6


def test_recursive_function() -> None:
    @dalil.trace
    def factorial(n: int) -> int:
        """Return ``n`` factorial."""
        if n < 2:
            return 1
        return n * factorial(n - 1)

    assert factorial(5) == 120


def test_generator_function() -> None:
    @dalil.trace
    def countdown(n: int) -> Iterator[int]:
        """Yield ``n`` down to 1."""
        yield from range(n, 0, -1)

    assert list(countdown(3)) == [3, 2, 1]


def test_async_function() -> None:
    @dalil.trace
    async def fetch() -> int:
        """Return 7."""
        return 7

    assert asyncio.run(fetch()) == 7


def test_lambda() -> None:
    wrapped = dalil.trace(lambda x: x * 2)
    assert wrapped(21) == 42


def test_nested_function() -> None:
    @dalil.trace
    def outer(x: int) -> int:
        """Call a decorated nested function."""

        @dalil.trace
        def inner(y: int) -> int:
            """Return ``y`` plus one."""
            return y + 1

        return inner(x)

    assert outer(1) == 2


def test_method_of_a_class() -> None:
    class Accumulator:
        """Sum values across calls."""

        def __init__(self) -> None:
            """Start from zero."""
            self.total = 0

        @dalil.trace
        def add(self, x: int) -> int:
            """Add ``x`` to the running total and return it."""
            self.total += x
            return self.total

    acc = Accumulator()
    assert acc.add(2) == 2
    assert acc.add(3) == 5
    assert acc.total == 5


def test_static_style_call_through_the_class() -> None:
    class Tools:
        """Namespace for a decorated method."""

        @dalil.trace
        def double(self, x: int) -> int:
            """Return ``x`` doubled."""
            return x * 2

    assert Tools.double(Tools(), 21) == 42


def test_exception_propagates_unchanged() -> None:
    error = ValueError("original message")

    @dalil.trace
    def boom() -> None:
        """Raise a ``ValueError``."""
        raise error

    with pytest.raises(ValueError) as excinfo:
        boom()
    assert excinfo.value is error


def test_exception_from_generator_propagates() -> None:
    @dalil.trace
    def broken() -> Iterator[int]:
        """Yield 1 then raise."""
        yield 1
        raise RuntimeError("generator failure")

    iterator = broken()
    assert next(iterator) == 1
    with pytest.raises(RuntimeError, match="generator failure"):
        next(iterator)


def test_stacked_decorators_below() -> None:
    @dalil.trace
    @plain_decorator
    def double(x: int) -> int:
        """Return ``x`` doubled."""
        return x * 2

    assert double(4) == 8
    assert isinstance(double, TracedFunction)


def test_stacked_decorators_above() -> None:
    @plain_decorator
    @dalil.trace
    def triple(x: int) -> int:
        """Return ``x`` tripled."""
        return x * 3

    assert triple(3) == 9


def test_stacked_three_layers() -> None:
    @dalil.trace
    @plain_decorator
    @dalil.trace
    def identity(x: int) -> int:
        """Return ``x`` unchanged."""
        return x

    assert identity(11) == 11


def test_repeated_calls_do_not_leak_state() -> None:
    wrapped = dalil.trace(samples.fibonacci)
    results = [wrapped(10) for _ in range(100)]
    assert results == [55] * 100


def test_concurrent_calls_do_not_leak_state() -> None:
    wrapped = dalil.trace(samples.bubble_sort)

    def sort_three(n: int) -> list[int]:
        """Sort a four-element list ending with ``n``."""
        return wrapped([3, 1, 2, n])

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(sort_three, range(32)))
    assert results == [sorted([3, 1, 2, n]) for n in range(32)]


def test_concurrent_calls_keep_the_same_return_value() -> None:
    wrapped = dalil.trace(samples.fibonacci)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(wrapped, [10] * 64))
    assert results == [55] * 64


def test_sys_settrace_unchanged_after_a_normal_call() -> None:
    previous = sys.gettrace()
    dalil.trace(samples.fibonacci)(10)
    assert sys.gettrace() is previous


def test_sys_settrace_unchanged_after_an_exception() -> None:
    previous = sys.gettrace()

    @dalil.trace
    def boom() -> None:
        """Raise a ``RuntimeError``."""
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        boom()
    assert sys.gettrace() is previous


def test_sys_settrace_unchanged_after_a_stub_error() -> None:
    previous = sys.gettrace()
    wrapped = dalil.trace(samples.fibonacci)
    calls: list[Callable[[], object]] = [
        lambda: wrapped.history,
        wrapped.flowchart,
        wrapped.complexity,
        wrapped.to_latex,
        lambda: wrapped.report("out.html"),
    ]
    for call in calls:
        with pytest.raises(NotImplementedError):
            call()
    assert sys.gettrace() is previous


def test_identity_of_wrapped_function_is_stable() -> None:
    def plain(x: int) -> int:
        """Return ``x`` unchanged."""
        return x

    wrapped = dalil.trace(plain)
    assert wrapped.__wrapped__ is plain
    assert wrapped.__wrapped__(1) == wrapped(1)
