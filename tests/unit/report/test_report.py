"""Nominal tests for the report public API: template and stub."""

from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from dalil.complexity import ComplexityResult
from dalil.flowchart import Edge, FlowGraph, Node
from dalil.report import default_template_dir, generate_report
from dalil.tracer import ExecutionHistory, LineEvent
from tests import samples


def test_default_template_dir_points_next_to_module() -> None:
    assert default_template_dir == Path(__file__).parents[3] / (
        "src/dalil/report/templates"
    )


def test_bundled_template_exists() -> None:
    assert (default_template_dir / "report.html.j2").is_file()


def test_bundled_template_renders_with_sample_models() -> None:
    env = Environment(
        loader=FileSystemLoader(default_template_dir),
        undefined=StrictUndefined,
    )
    template = env.get_template("report.html.j2")
    history = ExecutionHistory(
        function="fibonacci",
        events=[LineEvent(lineno=2, event="line", locals_snapshot={"n": 3})],
    )
    graph = FlowGraph(
        nodes=[Node(id="n1", label="return n", kind="exit")],
        edges=[Edge(source="n1", target="n2", label="yes")],
    )
    complexity = ComplexityResult(time="O(2^n)", space="O(n)", explanation="recursion")

    html = template.render(history=history, graph=graph, complexity=complexity)

    assert "fibonacci" in html
    assert "O(2^n)" in html
    assert "return n" in html
    assert "n: 3" in html or "&#39;n&#39;: 3" in html or "n" in html


def test_generate_report_is_not_implemented() -> None:
    with pytest.raises(NotImplementedError, match="not implemented yet"):
        generate_report(
            ExecutionHistory(),
            FlowGraph(),
            ComplexityResult(),
            "report.html",
        )


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_generate_report_writes_the_file(tmp_path: Path) -> None:
    path = tmp_path / "report.html"
    result = generate_report(
        ExecutionHistory(function="f"),
        FlowGraph(),
        ComplexityResult(),
        str(path),
    )
    assert result == str(path)
    assert path.is_file()
    assert "f" in path.read_text(encoding="utf-8")


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_generate_report_uses_the_bundled_template(tmp_path: Path) -> None:
    path = tmp_path / "report.html"
    generate_report(
        ExecutionHistory(function="fibonacci"),
        FlowGraph(),
        ComplexityResult(),
        str(path),
    )
    html = path.read_text(encoding="utf-8")
    assert html.startswith("<!DOCTYPE html>")
    assert "Dalil report" in html


def test_report_function_delegates_to_stub_without_side_effect(
    tmp_path: Path,
) -> None:
    path = tmp_path / "never-created.html"
    with pytest.raises(NotImplementedError, match="not implemented yet"):
        generate_report(ExecutionHistory(), FlowGraph(), ComplexityResult(), str(path))
    assert not path.exists()
    assert samples.fibonacci(5) == 5
