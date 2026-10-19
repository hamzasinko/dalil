"""Nominal tests for the complexity public API: model and stub."""

from dataclasses import FrozenInstanceError

import pytest

from dalil.complexity import ComplexityResult, estimate
from tests import samples


def test_complexity_result_creation_and_equality() -> None:
    first = ComplexityResult(time="O(n)", space="O(1)", explanation="one loop")
    second = ComplexityResult(time="O(n)", space="O(1)", explanation="one loop")
    assert first == second
    assert first.time == "O(n)"
    assert first.space == "O(1)"
    assert first.explanation == "one loop"


def test_complexity_result_defaults() -> None:
    result = ComplexityResult()
    assert result.time == "unknown"
    assert result.space == "unknown"
    assert result.explanation == ""


def test_complexity_result_is_frozen() -> None:
    result = ComplexityResult()
    with pytest.raises(FrozenInstanceError):
        result.time = "O(n)"  # type: ignore[misc]


def test_estimate_is_not_implemented() -> None:
    with pytest.raises(NotImplementedError, match="not implemented yet"):
        estimate(samples.linear_sum)


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_estimate_detects_linear_time() -> None:
    result = estimate(samples.linear_sum)
    assert result.time == "O(n)"
    assert result.space == "O(1)"


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_estimate_detects_constant_time() -> None:
    def identity(x: int) -> int:
        """Return ``x`` unchanged."""
        return x

    assert estimate(identity).time == "O(1)"


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_estimate_explanation_mentions_the_dominant_construct() -> None:
    result = estimate(samples.bubble_sort)
    assert "loop" in result.explanation.lower()
    assert result.time == "O(n^2)"
