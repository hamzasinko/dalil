"""Static complexity estimation layer.

This layer analyses a function's AST (loops, branches, nesting depth,
recursion) and estimates its time and space complexity without running
the code, returning a :class:`ComplexityResult`.

Attributes:
    ComplexityResult: Time / space estimate with an explanation.
    estimate: Estimate the complexity of a function (stub).
"""

from dataclasses import dataclass

from dalil._types import ComplexityClass, FuncT

__all__ = ["ComplexityResult", "estimate"]


@dataclass(frozen=True)
class ComplexityResult:
    """Time and space complexity estimate of a function.

    Args:
        time: Estimated time complexity class.
        space: Estimated space complexity class.
        explanation: Human-readable justification of the estimate.

    Attributes:
        time: Estimated time complexity class.
        space: Estimated space complexity class.
        explanation: Human-readable justification of the estimate.
    """

    time: ComplexityClass = "unknown"
    space: ComplexityClass = "unknown"
    explanation: str = ""


def estimate(func: FuncT) -> ComplexityResult:
    """Estimate the time and space complexity of ``func``.

    Args:
        func: The function to analyse.

    Returns:
        The complexity estimate of ``func``.

    Raises:
        NotImplementedError: Always; this is a project skeleton.
    """
    raise NotImplementedError(
        "complexity.estimate is not implemented yet: this module is a project skeleton."
    )
