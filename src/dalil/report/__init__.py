"""HTML report layer.

This layer assembles the execution history, the flowchart graph and the
complexity estimate into the Jinja2 template bundled in the
``templates/`` directory, then writes the rendered HTML to disk.

Attributes:
    default_template_dir: Directory holding the bundled templates.
    generate_report: Render an HTML report from Dalil models (stub).
"""

from pathlib import Path

from dalil.complexity import ComplexityResult
from dalil.flowchart import FlowGraph
from dalil.tracer import ExecutionHistory

__all__ = ["generate_report", "default_template_dir"]

default_template_dir = Path(__file__).parent / "templates"
"""Directory holding the bundled templates."""


def generate_report(
    history: ExecutionHistory,
    graph: FlowGraph,
    complexity: ComplexityResult,
    path: str,
) -> str:
    """Render an HTML report from Dalil models and write it to ``path``.

    Args:
        history: Execution history of the traced call.
        graph: Flowchart graph of the traced function.
        complexity: Complexity estimate of the traced function.
        path: Filesystem path where the HTML report is written.

    Returns:
        The path of the written report, equal to ``path``.

    Raises:
        NotImplementedError: Always; this is a project skeleton.
    """
    raise NotImplementedError(
        "report.generate_report is not implemented yet: this module is a "
        "project skeleton."
    )
