"""Tests for ACT-005: fail-closed behavior in IntegrationPipeline.

Regression coverage for "Stop datasets silent success on exceptions"
(`ecosystem-v2-certification/MASTER_ACTION_LIST.md`): an unhandled exception
in the Planning or Export phase of the (non-artifact-driven) integration
pipeline must make :attr:`PipelineResult.success` ``False``, never a
silently-forced ``True``.
"""

from __future__ import annotations

from pathlib import Path
from types import MappingProxyType

import pytest

from generators.execution.builders.diagnostics.builder_diagnostics import (
    BuilderDiagnostics,
)
from generators.execution.config.export_config import ExportConfig
from generators.execution.config.generator_config import GeneratorConfig
from generators.execution.config.runtime_config import RuntimeConfig
from generators.execution.graph.builder import GraphBuilder
from generators.execution.graph.enums import NodeType
from generators.execution.graph.graph import ExecutionGraph
from generators.execution.graph.node import ExecutionNode
from generators.execution.graph.results.graph_build_result import GraphBuildResult
from generators.execution.graph.statistics import GraphStatistics
from generators.execution.integration.pipeline import IntegrationPipeline
from generators.execution.integration.pipeline_context import PipelineContext
from generators.execution.integration.pipeline_statistics import PipelineStatistics
from generators.execution.export.exporter import Exporter
from generators.execution.planning.planner import Planner


def _build_context(tmp_path: Path) -> PipelineContext:
    return PipelineContext(
        generator_config=GeneratorConfig(custom_settings=MappingProxyType({})),
        export_config=ExportConfig(output_directory=tmp_path),
        runtime_config=RuntimeConfig(),
        discovery_result={},  # no "artifact_records" -> exercises the legacy per-phase path
        pipeline_statistics=PipelineStatistics(),
    )


def _stub_graph_with_one_node(*_args: object, **_kwargs: object) -> GraphBuildResult:
    """Stand-in for ``GraphBuilder.build`` that always yields one node.

    Used so tests exercising the Planning/Export phases don't get short
    circuited by the legitimate (non-exceptional) "Graph contains no nodes"
    failure from :class:`StageBuilder`, which would otherwise happen before
    Planning/Export ever run given the minimal, node-less discovery input.
    """
    node = ExecutionNode(node_id="node_1", node_type=NodeType.STEP, payload=object())
    graph = ExecutionGraph(nodes=(node,), edges=())
    return GraphBuildResult(
        success=True,
        graph=graph,
        diagnostics=BuilderDiagnostics(),
        statistics=GraphStatistics(node_count=1, edge_count=0),
    )


class TestPlanningPhaseFailsClosed:
    def test_exception_in_planner_yields_failure_not_forced_success(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def _raise(*_args: object, **_kwargs: object) -> None:
            raise RuntimeError("boom-planning")

        monkeypatch.setattr(Planner, "plan", staticmethod(_raise))

        result = IntegrationPipeline.execute(_build_context(tmp_path))

        assert result.success is False
        assert any("boom-planning" in d for d in result.diagnostics)
        assert any("Planning phase raised an exception" in d for d in result.diagnostics)


class TestExportPhaseFailsClosed:
    def test_exception_in_exporter_yields_failure_not_forced_success(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def _raise(*_args: object, **_kwargs: object) -> None:
            raise RuntimeError("boom-export")

        monkeypatch.setattr(GraphBuilder, "build", staticmethod(_stub_graph_with_one_node))
        monkeypatch.setattr(Exporter, "export", staticmethod(_raise))

        result = IntegrationPipeline.execute(_build_context(tmp_path))

        assert result.success is False
        assert any("boom-export" in d for d in result.diagnostics)
        assert any("Export phase raised an exception" in d for d in result.diagnostics)
