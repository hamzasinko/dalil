"""Shared pytest fixtures for the Dalil test suite."""

from collections.abc import Callable

import pytest

import dalil
from dalil.decorator import TracedFunction
from tests import samples


@pytest.fixture
def fibonacci() -> Callable[[int], int]:
    """Return the plain Fibonacci sample function."""
    return samples.fibonacci


@pytest.fixture
def bubble_sort() -> Callable[[list[int]], list[int]]:
    """Return the plain bubble-sort sample function."""
    return samples.bubble_sort


@pytest.fixture
def binary_search() -> Callable[[list[int], int], int]:
    """Return the plain binary-search sample function."""
    return samples.binary_search


@pytest.fixture
def linear_sum() -> Callable[[int], int]:
    """Return the plain single-loop sample function."""
    return samples.linear_sum


@pytest.fixture
def traced_fibonacci() -> TracedFunction[int]:
    """Return the Fibonacci sample wrapped by :func:`dalil.trace`."""
    return dalil.trace(samples.fibonacci)


@pytest.fixture
def traced_bubble_sort() -> TracedFunction[list[int]]:
    """Return the bubble-sort sample wrapped by :func:`dalil.trace`."""
    return dalil.trace(samples.bubble_sort)


@pytest.fixture
def traced_binary_search() -> TracedFunction[int]:
    """Return the binary-search sample wrapped by :func:`dalil.trace`."""
    return dalil.trace(samples.binary_search)
