"""Nominal tests for the :mod:`dalil.exceptions` hierarchy."""

from typing import Any

import pytest

from dalil.exceptions import (
    ComplexityError,
    DalilError,
    FlowchartError,
    LatexError,
    ReportError,
    TraceError,
)

ALL_ERRORS: list[type[DalilError]] = [
    TraceError,
    FlowchartError,
    ComplexityError,
    ReportError,
    LatexError,
]


@pytest.mark.parametrize("exc_type", ALL_ERRORS)
def test_every_error_derives_from_dalil_error(exc_type: type) -> None:
    assert issubclass(exc_type, DalilError)
    assert issubclass(exc_type, Exception)


def test_dalil_error_is_the_only_base() -> None:
    for exc_type in ALL_ERRORS:
        assert exc_type.__mro__[1] is DalilError


def test_dalil_error_stores_message() -> None:
    err = DalilError("something broke")
    assert err.message == "something broke"
    assert str(err) == "something broke"


def test_dalil_error_stores_cause() -> None:
    cause = ValueError("boom")
    err = DalilError("wrapped", cause=cause)
    assert err.cause is cause


def test_dalil_error_cause_defaults_to_none() -> None:
    assert DalilError("wrapped").cause is None


@pytest.mark.parametrize("exc_type", ALL_ERRORS)
def test_catching_base_class_catches_every_error(exc_type: Any) -> None:
    with pytest.raises(DalilError) as excinfo:
        raise exc_type("layer failure")
    assert excinfo.value.message == "layer failure"


def test_errors_are_raised_and_caught_across_layers() -> None:
    """Simulate layered usage: one layer wraps another's error."""
    with pytest.raises(ReportError) as outer:
        try:
            raise FlowchartError("bad AST")
        except FlowchartError as inner:
            raise ReportError("render failed", cause=inner) from inner
    assert isinstance(outer.value.cause, FlowchartError)
    assert outer.value.__cause__ is outer.value.cause
