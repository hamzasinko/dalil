"""Flowchart layer: AST -> graph model -> DOT / Mermaid / SVG.

This layer parses a function's source into an abstract syntax tree,
converts it into a portable :class:`FlowGraph` of :class:`Node` and
:class:`Edge` models, and renders that model as DOT or Mermaid source
(with SVG available through the optional ``graphviz`` extra).

Attributes:
    Node: One vertex of the flowchart graph.
    Edge: One directed link between two nodes.
    FlowGraph: Container holding every node and edge.
    build_flowgraph: Build a graph model from a function (stub).
    to_dot: Render a graph model as Graphviz DOT source (stub).
    to_mermaid: Render a graph model as Mermaid source (stub).
"""

from dataclasses import dataclass, field

from dalil._types import EdgeLabel, FuncT, NodeId

__all__ = [
    "Node",
    "Edge",
    "FlowGraph",
    "build_flowgraph",
    "to_dot",
    "to_mermaid",
]


@dataclass(frozen=True)
class Node:
    """One vertex of the flowchart graph.

    Args:
        id: Unique identifier of the node inside the graph.
        label: Human-readable text displayed in the node.
        kind: Node category such as ``entry``, ``exit``,
            ``decision`` or ``statement``.

    Attributes:
        id: Unique identifier of the node.
        label: Human-readable text displayed in the node.
        kind: Node category.
    """

    id: NodeId
    label: str
    kind: str = "statement"


@dataclass(frozen=True)
class Edge:
    """One directed link between two flowchart nodes.

    Args:
        source: Identifier of the node the edge starts from.
        target: Identifier of the node the edge points to.
        label: Human-readable label, e.g. ``"yes"`` / ``"no"``.

    Attributes:
        source: Identifier of the origin node.
        target: Identifier of the target node.
        label: Human-readable label of the edge.
    """

    source: NodeId
    target: NodeId
    label: EdgeLabel = ""


@dataclass
class FlowGraph:
    """Container holding every node and edge of a flowchart.

    Args:
        nodes: Nodes of the graph.
        edges: Directed edges of the graph.

    Attributes:
        nodes: Nodes of the graph.
        edges: Directed edges of the graph.
    """

    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)


def build_flowgraph(func: FuncT) -> FlowGraph:
    """Build a :class:`FlowGraph` from a function's AST.

    Args:
        func: The function to convert.

    Returns:
        The graph model of ``func``.

    Raises:
        NotImplementedError: Always; this is a project skeleton.
    """
    raise NotImplementedError(
        "flowchart.build_flowgraph is not implemented yet: this module is a "
        "project skeleton."
    )


def to_dot(graph: FlowGraph) -> str:
    """Render a :class:`FlowGraph` as Graphviz DOT source.

    Args:
        graph: The graph to render.

    Returns:
        The DOT source of the flowchart.

    Raises:
        NotImplementedError: Always; this is a project skeleton.
    """
    raise NotImplementedError(
        "flowchart.to_dot is not implemented yet: this module is a project skeleton."
    )


def to_mermaid(graph: FlowGraph) -> str:
    """Render a :class:`FlowGraph` as Mermaid source.

    Args:
        graph: The graph to render.

    Returns:
        The Mermaid source of the flowchart.

    Raises:
        NotImplementedError: Always; this is a project skeleton.
    """
    raise NotImplementedError(
        "flowchart.to_mermaid is not implemented yet: this module is a "
        "project skeleton."
    )
