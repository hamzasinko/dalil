"""Line-by-line execution tracing layer.

This layer models the events collected while a function runs: one
:class:`LineEvent` per executed line, gathered into an
:class:`ExecutionHistory` by the :class:`Tracer` context manager. The
tracer must always restore ``sys.settrace``, even when an exception
escapes the traced call.

Attributes:
    LineEvent: A single recorded execution event.
    ExecutionHistory: Ordered events of one function execution.
    Tracer: Context manager collecting events for one call (stub).
"""

from dataclasses import dataclass, field
from time import time
from types import TracebackType
from typing import Optional

from dalil._types import FuncT, TraceEventName

__all__ = ["LineEvent", "ExecutionHistory", "Tracer"]


@dataclass(frozen=True)
class LineEvent:
    """A single execution event recorded on one source line.

    Args:
        lineno: Source line number that produced the event.
        event: Kind of tracing event (``line``, ``return``, ...).
        locals_snapshot: Copy of the local variables at that moment.
        timestamp: Unix time at which the event was recorded.

    Attributes:
        lineno: Source line number that produced the event.
        event: Kind of tracing event.
        locals_snapshot: Copy of the local variables.
        timestamp: Unix time of the event.
    """

    lineno: int
    event: TraceEventName
    locals_snapshot: dict[str, object] = field(default_factory=dict)
    timestamp: float = field(default_factory=time)


@dataclass
class ExecutionHistory:
    """Ordered events recorded during one function execution.

    Args:
        function: Qualified name of the traced function.
        events: Recorded events, in execution order.

    Attributes:
        function: Qualified name of the traced function.
        events: Recorded events, in execution order.
    """

    function: str = "<unknown>"
    events: list[LineEvent] = field(default_factory=list)

    def add(self, event: LineEvent) -> None:
        """Append ``event`` to the recorded history.

        Args:
            event: The event to record.
        """
        self.events.append(event)


class Tracer:
    """Context manager collecting events for one function call (stub).

    Args:
        func: The function whose execution is being traced.

    Attributes:
        func: The function whose execution is being traced.
        history: History populated during the ``with`` block.
    """

    def __init__(self, func: FuncT) -> None:
        """Initialize the tracer for ``func``.

        Args:
            func: The function whose execution is being traced.
        """
        self.func = func
        self.history = ExecutionHistory(
            function=getattr(func, "__qualname__", "<unknown>")
        )

    def __enter__(self) -> "Tracer":
        """Start collecting events.

        Returns:
            This tracer, so the ``with`` block can bind it.

        Raises:
            NotImplementedError: Always; this is a project skeleton.
        """
        raise NotImplementedError(
            "tracer.Tracer is not implemented yet: this module is a project skeleton."
        )

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        """Stop collecting events and restore the previous trace hook.

        Args:
            exc_type: Type of the exception leaving the block, if any.
            exc_value: Exception leaving the block, if any.
            traceback: Traceback of the exception, if any.

        Returns:
            ``False`` so exceptions are never swallowed.

        Raises:
            NotImplementedError: Always; this is a project skeleton.
        """
        raise NotImplementedError(
            "tracer.Tracer is not implemented yet: this module is a project skeleton."
        )
