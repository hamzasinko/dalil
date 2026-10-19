"""Nominal tests for the flowchart public API: models and stubs."""

from dataclasses import FrozenInstanceError

import pytest
from hypothesis import given
from hypothesis import strategies as st

from dalil.flowchart import Edge, FlowGraph, Node, build_flowgraph, to_dot, to_mermaid
from tests import samples


def test_node_creation_and_equality() -> None:
    first = Node(id="n1", label="return x", kind="exit")
    second = Node(id="n1", label="return x", kind="exit")
    assert first == second
    assert first.id == "n1"
    assert first.label == "return x"
    assert first.kind == "exit"


def test_node_default_kind_is_statement() -> None:
    assert Node(id="n1", label="x = 1").kind == "statement"


def test_node_is_frozen() -> None:
    node = Node(id="n1", label="x = 1")
    with pytest.raises(FrozenInstanceError):
        node.label = "y = 2"  # type: ignore[misc]


def test_edge_creation_and_equality() -> None:
    first = Edge(source="n1", target="n2", label="yes")
    second = Edge(source="n1", target="n2", label="yes")
    assert first == second
    assert first.label == "yes"


def test_edge_default_label_is_empty() -> None:
    assert Edge(source="n1", target="n2").label == ""


def test_edge_is_frozen() -> None:
    edge = Edge(source="n1", target="n2")
    with pytest.raises(FrozenInstanceError):
        edge.source = "n9"  # type: ignore[misc]


def test_flow_graph_starts_empty() -> None:
    graph = FlowGraph()
    assert graph.nodes == []
    assert graph.edges == []


def test_flow_graph_instances_do_not_share_lists() -> None:
    first = FlowGraph()
    second = FlowGraph()
    first.nodes.append(Node(id="n1", label="entry", kind="entry"))
    assert second.nodes == []


def test_flow_graph_collects_nodes_and_edges() -> None:
    node = Node(id="n1", label="entry", kind="entry")
    graph = FlowGraph(nodes=[node], edges=[Edge(source="n1", target="n2", label="yes")])
    assert graph.nodes == [node]
    assert graph.edges[0].label == "yes"


def test_build_flowgraph_is_not_implemented() -> None:
    with pytest.raises(NotImplementedError, match="not implemented yet"):
        build_flowgraph(samples.fibonacci)


def test_to_dot_is_not_implemented() -> None:
    with pytest.raises(NotImplementedError, match="not implemented yet"):
        to_dot(FlowGraph())


def test_to_mermaid_is_not_implemented() -> None:
    with pytest.raises(NotImplementedError, match="not implemented yet"):
        to_mermaid(FlowGraph())


@given(st.integers(min_value=0, max_value=100), st.text(max_size=20))
def test_node_roundtrips_through_equality(node_id: int, label: str) -> None:
    node = Node(id=f"n{node_id}", label=label)
    assert Node(id=f"n{node_id}", label=label) == node


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_build_flowgraph_has_entry_and_exit() -> None:
    graph = build_flowgraph(samples.fibonacci)
    kinds = {node.kind for node in graph.nodes}
    assert "entry" in kinds
    assert "exit" in kinds


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_build_flowgraph_links_decision_branches() -> None:
    graph = build_flowgraph(samples.fibonacci)
    labels = {edge.label for edge in graph.edges}
    assert {"yes", "no"} <= labels


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_to_dot_emits_digraph() -> None:
    assert to_dot(build_flowgraph(samples.fibonacci)).startswith("digraph")


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_to_mermaid_emits_flowchart() -> None:
    assert to_mermaid(build_flowgraph(samples.fibonacci)).startswith("flowchart")
