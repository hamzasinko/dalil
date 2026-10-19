"""Shared type aliases and protocols used across Dalil subpackages.

This module is intentionally dependency-free so that every layer
(``tracer``, ``flowchart``, ``complexity``, ``report``, ``latex``) can
import the same vocabulary without creating cross-package imports.

Attributes:
    FuncT: A callable accepted by the ``trace`` decorator.
    NodeId: Identifier of a node inside a flowchart graph model.
    EdgeLabel: Human-readable label attached to a flowchart edge.
    ComplexityClass: Big-O class estimated by the complexity layer.
    TraceEventName: Name of a low-level tracing event.
    Options: Mapping of user-facing options shared by all layers.
"""

from collections.abc import Mapping
from typing import Any, Callable, Literal, Protocol

__all__ = [
    "FuncT",
    "NodeId",
    "EdgeLabel",
    "ComplexityClass",
    "TraceEventName",
    "Options",
    "Renderable",
]

FuncT = Callable[..., Any]
"""A callable accepted by the :func:`dalil.trace` decorator."""

NodeId = str
"""Identifier of a node inside a flowchart graph model."""

EdgeLabel = str
"""Human-readable label attached to a flowchart edge."""

ComplexityClass = Literal[
    "O(1)",
    "O(log n)",
    "O(n)",
    "O(n log n)",
    "O(n^2)",
    "O(n^3)",
    "O(2^n)",
    "O(n!)",
    "unknown",
]
"""Big-O class estimated by the complexity layer."""

TraceEventName = Literal[
    "call",
    "line",
    "return",
    "exception",
    "opcode",
]
"""Name of a low-level tracing event produced by the tracer."""

Options = Mapping[str, Any]
"""Mapping of user-facing options shared by all layers."""


class Renderable(Protocol):
    """A model that can render itself to a portable text format.

    Methods:
        render: Return the rendered representation of the model.
    """

    def render(self) -> str:
        """Return the rendered representation of the model."""
        ...
