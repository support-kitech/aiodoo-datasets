"""Converts Phase 1 domain objects into an ExecutionGraph."""

from generators.execution.graph.graph import ExecutionGraph
from generators.execution.graph.node import ExecutionNode
from generators.execution.graph.edge import ExecutionEdge
from generators.execution.graph.enums import NodeType, EdgeType
from generators.execution.graph.context import GraphContext
from generators.execution.graph.results.graph_build_result import GraphBuildResult
from generators.execution.graph.statistics import GraphStatistics
from generators.execution.builders.diagnostics.builder_diagnostics import (
    BuilderDiagnostics,
)


class GraphBuilder:
    """
    Converts domain objects (ExecutionStep, ExecutionDependency) into
    ExecutionNode and ExecutionEdge instances, then assembles an ExecutionGraph.

    Never performs planning. Never sorts. Only builds the graph structure.
    """

    @staticmethod
    def build(context: GraphContext) -> GraphBuildResult:
        """Deterministically builds a graph from domain steps and dependencies."""
        nodes = []
        edges = []

        for step in context.domain_steps:
            node = ExecutionNode(
                node_id=step.step_id,
                node_type=NodeType.STEP,
                payload=step,
            )
            nodes.append(node)

            # Build edges from the step's dependencies
            for dep in step.dependencies:
                edge = ExecutionEdge(
                    source_id=dep.depends_on_step_id,
                    target_id=step.step_id,
                    edge_type=EdgeType.DEPENDENCY,
                )
                edges.append(edge)

        graph = ExecutionGraph(
            nodes=tuple(sorted(nodes)),
            edges=tuple(edges),
        )

        stats = GraphStatistics(
            node_count=len(nodes),
            edge_count=len(edges),
        )

        return GraphBuildResult(
            success=True,
            graph=graph,
            diagnostics=BuilderDiagnostics(),
            statistics=stats,
        )
