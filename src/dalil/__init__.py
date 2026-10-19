"""Dalil: a decorator that makes code execution understandable.

Dalil (Arabic for "guide") turns a plain Python function into a visual
flowchart, traces its execution line by line, estimates its algorithmic
complexity, and exports the result as an HTML report or LaTeX algorithm.

Example:
    >>> import dalil
    >>> @dalil.trace
    ... def binary_search(items, target):
    ...     ...
    ...

Attributes:
    __version__: The distribution version string of the package.
    trace: The public decorator that enables tracing on a function.
"""

from dalil.decorator import trace

__version__ = "0.1.0"

__all__ = ["__version__", "trace"]
