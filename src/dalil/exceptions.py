"""Custom exception hierarchy for Dalil.

Every error raised by Dalil derives from :class:`DalilError`, so callers
can catch a single base class. Never raise a bare ``Exception`` inside
the library.

Attributes:
    DalilError: Base class of every Dalil error.
    TraceError: Raised when execution tracing fails.
    FlowchartError: Raised when a flowchart cannot be built or rendered.
    ComplexityError: Raised when complexity estimation fails.
    ReportError: Raised when an HTML report cannot be generated.
    LatexError: Raised when LaTeX export fails.
"""

from typing import Optional

__all__ = [
    "DalilError",
    "TraceError",
    "FlowchartError",
    "ComplexityError",
    "ReportError",
    "LatexError",
]


class DalilError(Exception):
    """Base class of every error raised by Dalil.

    Args:
        message: Human-readable description of the failure.
        cause: Optional exception that triggered this error.

    Attributes:
        message: The description stored on the instance.
        cause: The chained original error, if any.
    """

    def __init__(self, message: str, cause: Optional[BaseException] = None) -> None:
        """Initialize the error with a message and an optional cause.

        Args:
            message: Human-readable description of the failure.
            cause: Optional exception that triggered this error.
        """
        super().__init__(message)
        self.message = message
        self.cause = cause


class TraceError(DalilError):
    """Raised when execution tracing fails.

    This covers failures while attaching ``sys.settrace``, while
    collecting events, or while restoring the previous trace function.
    """


class FlowchartError(DalilError):
    """Raised when a flowchart cannot be built or rendered.

    This covers unparsable source, unsupported AST nodes and DOT /
    Mermaid / SVG rendering failures.
    """


class ComplexityError(DalilError):
    """Raised when complexity estimation fails.

    This covers unsupported control-flow patterns and missing source
    code needed for a static analysis.
    """


class ReportError(DalilError):
    """Raised when an HTML report cannot be generated.

    This covers missing Jinja2 templates, context-serialization errors
    and filesystem write failures.
    """


class LatexError(DalilError):
    """Raised when LaTeX export fails.

    This covers unsupported statements and failures while emitting
    ``algorithm2e`` / ``algorithmicx`` source.
    """
