"""Public ``trace`` decorator.

The decorator supports both bare and called forms::

    @trace
    def f(...): ...

    @trace(report="out.html", latex=True)
    def g(...): ...

The returned wrapper keeps the original function's behavior, return
value and metadata (``functools.update_wrapper``) and additionally
exposes the Dalil API: ``.history``, ``.flowchart()``,
``.complexity()``, ``.to_latex()`` and ``.report(path)``. Those accessors
delegate to the layer modules, which are stubs for now.

Attributes:
    TracedFunction: Wrapper returned by :func:`trace`.
    trace: Decorator enabling Dalil inspection on a function.
"""

from functools import update_wrapper
from types import MethodType
from typing import Any, Callable, Generic, Optional, TypeVar, Union, overload

from dalil._types import FuncT
from dalil.complexity import ComplexityResult, estimate
from dalil.flowchart import FlowGraph, build_flowgraph
from dalil.latex import to_latex
from dalil.report import generate_report
from dalil.tracer import ExecutionHistory

__all__ = ["trace", "TracedFunction"]

_R = TypeVar("_R")


class TracedFunction(Generic[_R]):
    """Wrapper returned by :func:`dalil.trace`.

    Calling the wrapper behaves exactly like calling the original
    function; the inspection methods are stubs that delegate to the
    layer modules.

    Args:
        func: The original function being wrapped.
        report: Default path of the HTML report, if requested.
        latex: Whether LaTeX output was requested at decoration time.
        options: Extra layer-specific options captured at decoration.

    Attributes:
        __name__: Name of the wrapped function.
        __qualname__: Qualified name of the wrapped function.
        __doc__: Docstring of the wrapped function.
        __module__: Module of the wrapped function.
        __wrapped__: The original, undecorated function.
    """

    __name__: str
    __qualname__: str
    __doc__: Optional[str]
    __module__: str
    __wrapped__: Callable[..., _R]

    def __init__(
        self,
        func: Callable[..., _R],
        report: Optional[str] = None,
        latex: bool = False,
        options: Optional[dict[str, Any]] = None,
    ) -> None:
        """Wrap ``func`` while preserving its metadata.

        Args:
            func: The original function being wrapped.
            report: Default path of the HTML report, if requested.
            latex: Whether LaTeX output was requested.
            options: Extra layer-specific options.
        """
        self._func = func
        self._report = report
        self._latex = latex
        self._options: dict[str, Any] = dict(options or {})
        update_wrapper(self, func)

    def __call__(self, *args: Any, **kwargs: Any) -> _R:
        """Call the wrapped function unchanged.

        Args:
            *args: Positional arguments forwarded to the function.
            **kwargs: Keyword arguments forwarded to the function.

        Returns:
            Whatever the original function returns.
        """
        return self._func(*args, **kwargs)

    def __get__(
        self, instance: Optional[object], owner: Optional[type] = None
    ) -> Union["TracedFunction[_R]", MethodType]:
        """Bind the wrapper as a method when accessed from a class.

        This keeps decorated methods working: without the descriptor
        protocol, ``instance.method(args)`` would not receive the
        instance as first argument.

        Args:
            instance: The instance the attribute was accessed from, or
                ``None`` when accessed through the class.
            owner: The class through which the attribute was accessed.

        Returns:
            ``self`` when accessed from the class, otherwise a bound
            method passing ``instance`` as first argument.
        """
        if instance is None:
            return self
        return MethodType(self, instance)

    @property
    def history(self) -> ExecutionHistory:
        """Execution history of the traced calls.

        Raises:
            NotImplementedError: Always; the tracer is a stub.
        """
        raise NotImplementedError(
            "TracedFunction.history is not implemented yet: the tracer is a "
            "project skeleton."
        )

    def flowchart(self) -> FlowGraph:
        """Flowchart graph of the wrapped function.

        Returns:
            The graph model built from the function's AST.

        Raises:
            NotImplementedError: Always; the flowchart layer is a stub.
        """
        return build_flowgraph(self._func)

    def complexity(self) -> ComplexityResult:
        """Complexity estimate of the wrapped function.

        Returns:
            The time / space estimate of the function.

        Raises:
            NotImplementedError: Always; the complexity layer is a stub.
        """
        return estimate(self._func)

    def to_latex(self) -> str:
        """LaTeX algorithm source of the wrapped function.

        Returns:
            The LaTeX source of the function.

        Raises:
            NotImplementedError: Always; the LaTeX layer is a stub.
        """
        return to_latex(self._func)

    def report(self, path: str) -> str:
        """Render the HTML report of the wrapped function.

        Args:
            path: Filesystem path where the report is written.

        Returns:
            The path of the written report.

        Raises:
            NotImplementedError: Always; the report layer is a stub.
        """
        return generate_report(self.history, self.flowchart(), self.complexity(), path)


def _make_decorator(
    report: Optional[str],
    latex: bool,
    options: dict[str, Any],
) -> Callable[[FuncT], TracedFunction[Any]]:
    """Build the decorator returned when ``trace`` is called without a function.

    Args:
        report: Default path of the HTML report.
        latex: Whether LaTeX output was requested.
        options: Extra layer-specific options.

    Returns:
        A decorator applying :class:`TracedFunction` to a function.
    """

    def decorator(target: FuncT) -> TracedFunction[Any]:
        """Wrap ``target`` with :class:`TracedFunction`.

        Args:
            target: The function to decorate.

        Returns:
            The wrapped function.
        """
        return TracedFunction(target, report=report, latex=latex, options=options)

    return decorator


@overload
def trace(func: Callable[..., _R]) -> TracedFunction[_R]: ...


@overload
def trace(
    func: None = None,
    *,
    report: Optional[str] = None,
    latex: bool = False,
    **options: Any,
) -> Callable[[Callable[..., _R]], TracedFunction[_R]]: ...


def trace(
    func: Optional[FuncT] = None,
    *,
    report: Optional[str] = None,
    latex: bool = False,
    **options: Any,
) -> Any:
    """Enable Dalil inspection on a function.

    Supports both ``@trace`` and ``@trace(...)`` call styles. The
    decorated function keeps its original behavior, return value and
    metadata.

    Args:
        func: The function to decorate when used without parentheses.
        report: Default path of the HTML report to generate.
        latex: Whether a LaTeX export should be generated.
        **options: Extra layer-specific options.

    Returns:
        The wrapped function when used as ``@trace``, otherwise a
        decorator awaiting the function.
    """
    if func is None:
        return _make_decorator(report, latex, options)
    return TracedFunction(func, report=report, latex=latex, options=options)
