"""LaTeX export layer.

This layer converts a function's AST into a LaTeX algorithm using the
``algorithm2e`` or ``algorithmicx`` style, ready to be embedded in a
paper or a course handout.

Attributes:
    to_latex: Convert a function into LaTeX algorithm source (stub).
"""

from dalil._types import FuncT

__all__ = ["to_latex"]


def to_latex(func: FuncT) -> str:
    """Convert ``func`` into LaTeX algorithm source.

    Args:
        func: The function to convert.

    Returns:
        The LaTeX source of the algorithm.

    Raises:
        NotImplementedError: Always; this is a project skeleton.
    """
    raise NotImplementedError(
        "latex.to_latex is not implemented yet: this module is a project skeleton."
    )
