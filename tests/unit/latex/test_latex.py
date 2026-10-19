"""Nominal tests for the latex public API: stub."""

import pytest

from dalil.latex import to_latex
from tests import samples


def test_to_latex_is_not_implemented() -> None:
    with pytest.raises(NotImplementedError, match="not implemented yet"):
        to_latex(samples.fibonacci)


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_to_latex_emits_algorithm_environment() -> None:
    source = to_latex(samples.fibonacci)
    assert "\\begin{algorithm}" in source
    assert "\\caption" in source


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_to_latex_keeps_the_function_name() -> None:
    source = to_latex(samples.fibonacci)
    assert "fibonacci" in source


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_to_latex_renders_the_recursive_call() -> None:
    source = to_latex(samples.fibonacci)
    assert "fibonacci(" in source
