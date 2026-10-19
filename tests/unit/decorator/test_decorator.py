"""Nominal tests for the public ``trace`` decorator."""

from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

import dalil
from dalil.complexity import ComplexityResult
from dalil.decorator import TracedFunction
from dalil.flowchart import FlowGraph
from dalil.tracer import ExecutionHistory
from tests import samples


def collect(*args: int, **kwargs: int) -> tuple[tuple[int, ...], dict[str, int]]:
    """Return the arguments that were forwarded."""
    return args, kwargs


class Calculator:
    """Minimal class used to test decorated methods."""

    @dalil.trace
    def double(self, x: int) -> int:
        """Return ``x`` doubled."""
        return x * 2


def test_package_exposes_version() -> None:
    assert dalil.__version__ == "0.1.0"


def test_trace_is_exported() -> None:
    assert callable(dalil.trace)


def test_bare_form_wraps_and_keeps_return_value(
    traced_fibonacci: TracedFunction[int],
) -> None:
    assert isinstance(traced_fibonacci, TracedFunction)
    assert traced_fibonacci(10) == 55
    assert traced_fibonacci(10) == samples.fibonacci(10)


def test_called_form_wraps_and_keeps_return_value() -> None:
    decorator = dalil.trace(report="out.html", latex=True)
    wrapped = decorator(samples.fibonacci)
    assert isinstance(wrapped, TracedFunction)
    assert wrapped(10) == 55


def test_called_form_without_arguments() -> None:
    wrapped = dalil.trace()(samples.fibonacci)
    assert wrapped(6) == 8


def test_wraps_preserves_metadata() -> None:
    wrapped = dalil.trace(samples.fibonacci)
    assert wrapped.__name__ == "fibonacci"
    assert wrapped.__qualname__ == "fibonacci"
    assert wrapped.__doc__ == "Return the n-th Fibonacci number (naive recursion)."
    assert wrapped.__module__ == "tests.samples"
    assert wrapped.__wrapped__ is samples.fibonacci


def test_positional_arguments_are_forwarded() -> None:
    wrapped = dalil.trace(collect)
    assert wrapped(1, 2, 3) == ((1, 2, 3), {})


def test_keyword_arguments_are_forwarded() -> None:
    wrapped = dalil.trace(collect)
    assert wrapped(a=1, b=2) == ((), {"a": 1, "b": 2})


def test_mixed_arguments_are_forwarded() -> None:
    wrapped = dalil.trace(collect)
    assert wrapped(1, 2, a=3) == ((1, 2), {"a": 3})


def test_default_arguments_are_forwarded() -> None:
    def scale(x: int, factor: int = 2) -> int:
        """Return ``x`` scaled by ``factor``."""
        return x * factor

    wrapped = dalil.trace(scale)
    assert wrapped(3) == 6
    assert wrapped(3, factor=5) == 15


def test_decorated_method_keeps_binding() -> None:
    assert Calculator().double(21) == 42


def test_decorated_method_accessed_from_class() -> None:
    calc = Calculator()
    assert Calculator.double(calc, 21) == 42
    assert isinstance(Calculator.double, TracedFunction)


def test_options_are_captured_at_decoration_time() -> None:
    decorator: Callable[[Callable[..., int]], TracedFunction[int]] = dalil.trace(
        report="out.html", latex=True, depth=3
    )
    wrapped = decorator(samples.fibonacci)
    assert wrapped._report == "out.html"
    assert wrapped._latex is True
    assert wrapped._options == {"depth": 3}


@given(st.integers(min_value=0, max_value=18))
def test_fibonacci_return_value_is_unchanged(n: int) -> None:
    wrapped = dalil.trace(samples.fibonacci)
    assert wrapped(n) == samples.fibonacci(n)


@given(st.lists(st.integers(min_value=-1000, max_value=1000), max_size=25))
def test_bubble_sort_return_value_is_unchanged(items: list[int]) -> None:
    wrapped = dalil.trace(samples.bubble_sort)
    assert wrapped(list(items)) == samples.bubble_sort(list(items))


@given(
    st.lists(st.integers(min_value=-100, max_value=100), max_size=25).map(sorted),
    st.integers(min_value=-150, max_value=150),
)
def test_binary_search_return_value_is_unchanged(items: list[int], target: int) -> None:
    wrapped = dalil.trace(samples.binary_search)
    assert wrapped(items, target) == samples.binary_search(items, target)


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_history_returns_execution_history(
    traced_fibonacci: TracedFunction[int],
) -> None:
    traced_fibonacci(5)
    history = traced_fibonacci.history
    assert isinstance(history, ExecutionHistory)
    assert history.function == "fibonacci"
    assert history.events


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_flowchart_returns_flow_graph(
    traced_fibonacci: TracedFunction[int],
) -> None:
    graph = traced_fibonacci.flowchart()
    assert isinstance(graph, FlowGraph)
    assert graph.nodes


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_complexity_returns_complexity_result(
    traced_fibonacci: TracedFunction[int],
) -> None:
    result = traced_fibonacci.complexity()
    assert isinstance(result, ComplexityResult)
    assert result.time != "unknown"


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_to_latex_returns_source(traced_fibonacci: TracedFunction[int]) -> None:
    source = traced_fibonacci.to_latex()
    assert isinstance(source, str)
    assert "fibonacci" in source


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_report_writes_html_file(
    traced_fibonacci: TracedFunction[int], tmp_path: Path
) -> None:
    path = tmp_path / "fibonacci.html"
    result = traced_fibonacci.report(str(path))
    assert result == str(path)
    assert path.is_file()
    assert path.read_text(encoding="utf-8").startswith("<!DOCTYPE html>")


def test_any_return_type_is_preserved() -> None:
    def identity(x: Any) -> Any:
        """Return ``x`` unchanged."""
        return x

    wrapped = dalil.trace(identity)
    sentinel = object()
    assert wrapped(sentinel) is sentinel
