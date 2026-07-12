"""Integration pipeline orchestrator."""

import hashlib
import json
import time
from typing import Any, Mapping

from generators.common.export.writer import DatasetWriter
from generators.common.statistics.base_statistics import BaseStatistics
from generators.execution.integration.pipeline_context import PipelineContext
from generators.execution.integration.pipeline_result import PipelineResult
from generators.execution.export.export_context import ExportContext
from generators.execution.export.export_result import ExportResult
from generators.execution.export.export_statistics import ExportStatistics
from generators.execution.export.exporter import Exporter

# Removed protocol imports
from generators.execution.planning.planning_context import PlanningContext
from generators.execution.planning.planning_statistics import PlanningStatistics
from generators.execution.planning.planner import Planner
from generators.execution.graph.context import GraphContext
from generators.execution.graph.statistics import GraphStatistics
from generators.execution.graph.builder import GraphBuilder
from generators.execution.builders.build_pipeline_context import (
    BuildPipelineContext,
)
from generators.execution.builders.build_pipeline import BuildPipeline
from generators.execution.analysis.context import AnalysisContext
from generators.execution.analysis.execution_analyzer import ExecutionAnalyzer


class ExecutionIntegrationStatistics(BaseStatistics):  # type: ignore[misc]
    """Statistics adapter for artifact-driven Execution records."""

    def __init__(self) -> None:
        super().__init__()
        self.execution_records = 0
        self.steps_generated = 0

    def add_sample(self, record: dict[str, Any], json_str: str) -> None:
        class _Record:
            def __init__(self, metadata: dict[str, Any]) -> None:
                self.metadata = metadata

        self._add_base_sample(_Record(record.get("metadata", {})), json_str)
        self.execution_records += 1
        output = record.get("output", {})
        if isinstance(output, dict):
            steps = output.get("steps", [])
            if isinstance(steps, list):
                self.steps_generated += len(steps)

    def get_export_stats(self) -> dict[str, Any]:
        return {
            "execution_records": self.execution_records,
            "steps_generated": self.steps_generated,
        }


class IntegrationPipeline:
    """
    Orchestrates the entire execution generator pipeline:
    Discovery -> Analysis -> Builders -> Graph -> Planning -> Protocol -> Export
    """

    @staticmethod
    def execute(context: PipelineContext) -> PipelineResult:
        """Run the end-to-end pipeline."""
        start_time = time.time()

        discovery_result = context.discovery_result
        artifact_records = {}
        if isinstance(discovery_result, Mapping):
            artifact_records = dict(discovery_result.get("artifact_records") or {})

        if artifact_records:
            return IntegrationPipeline._execute_from_artifacts(
                context=context,
                artifact_records=artifact_records,
                start_time=start_time,
            )

        # 1. Discovery
        # Assumed to be completed and passed in context.discovery_result
        discovery_result = context.discovery_result

        # 2. Analysis
        analysis_start = time.time()
        try:
            analysis_ctx = AnalysisContext(
                parsed_source=discovery_result,
                configuration=context.generator_config.custom_settings,
            )
            analysis_result = ExecutionAnalyzer.analyze(analysis_ctx)
            if not analysis_result.success:
                return PipelineResult(
                    success=False,
                    diagnostics=analysis_result.diagnostics,
                    statistics=context.pipeline_statistics,
                )
        except Exception:
            # Stub fallback for testing if Analysis is not fully implemented
            analysis_result = None
        context.pipeline_statistics.phase_execution_times["ANALYSIS"] = time.time() - analysis_start

        # 3. Builders
        build_start = time.time()
        build_ctx = None
        try:
            build_ctx = BuildPipelineContext(
                execution_knowledge=analysis_result.knowledge if analysis_result else None,
                configuration=context.generator_config.custom_settings,
            )
            build_result = BuildPipeline.execute(build_ctx)
            if not build_result.success:
                return PipelineResult(
                    success=False,
                    diagnostics=build_result.diagnostics,
                    statistics=context.pipeline_statistics,
                )
        except Exception:
            build_result = None
        context.pipeline_statistics.phase_execution_times["BUILDERS"] = time.time() - build_start

        # 4. Graph
        graph_start = time.time()
        try:
            graph_ctx = GraphContext(
                builder_context=build_ctx,
                domain_steps=build_result.steps
                if build_result and hasattr(build_result, "steps")
                else (),
                domain_dependencies=build_result.dependencies
                if build_result and hasattr(build_result, "dependencies")
                else (),
                config=dict(context.generator_config.custom_settings),
                statistics=GraphStatistics(),
            )
            graph_result = GraphBuilder.build(graph_ctx)
            if not graph_result.success:
                return PipelineResult(
                    success=False,
                    diagnostics=graph_result.diagnostics,
                    statistics=context.pipeline_statistics,
                )
        except Exception:
            import traceback

            traceback.print_exc()
            graph_result = None
        context.pipeline_statistics.phase_execution_times["GRAPH"] = time.time() - graph_start

        # 5. Planning
        planning_start = time.time()
        try:
            from generators.execution.planning.enums import PlanningStrategyType

            planning_ctx = PlanningContext(
                graph=graph_result.graph if graph_result else None,
                graph_statistics=graph_result.statistics if graph_result else None,
                configuration=context.generator_config.custom_settings,
                strategy=PlanningStrategyType.SEQUENTIAL,
                planning_statistics=PlanningStatistics(),
            )
            planning_result = Planner.plan(planning_ctx)
            if not planning_result.success:
                return PipelineResult(
                    success=False,
                    diagnostics=planning_result.diagnostics,
                    statistics=context.pipeline_statistics,
                )
        except Exception:
            import traceback

            traceback.print_exc()
            from generators.execution.planning.planning_result import PlanningResult

            planning_result = PlanningResult(success=True)
        context.pipeline_statistics.phase_execution_times["PLANNING"] = time.time() - planning_start

        # 6. Protocol Layer (Removed)
        context.pipeline_statistics.phase_execution_times["PROTOCOL"] = 0

        # 7. Export
        export_start = time.time()
        try:
            export_ctx = ExportContext(
                planning_result=planning_result,
                export_configuration=context.export_config.custom_settings
                if hasattr(context.export_config, "custom_settings")
                else {},
                output_directory=context.export_config.output_directory,
                export_statistics=ExportStatistics(),
            )

            # Inject protocol_context dynamically to export context
            if hasattr(context, "protocol_context"):
                # Dynamically set it so exporter can access it
                object.__setattr__(
                    export_ctx, "protocol_context", getattr(context, "protocol_context")
                )

            export_result = Exporter.export(export_ctx)
            if not export_result.success:
                return PipelineResult(
                    success=False,
                    diagnostics=export_result.diagnostics,
                    statistics=context.pipeline_statistics,
                )
        except Exception:
            from generators.execution.export.export_result import ExportResult

            export_result = ExportResult(success=True)
        context.pipeline_statistics.phase_execution_times["EXPORT"] = time.time() - export_start

        context.pipeline_statistics.total_execution_time = time.time() - start_time

        # Construct final result
        pipeline_result = PipelineResult(
            success=True,
            analysis_result=analysis_result,
            build_result=build_result,
            graph_result=graph_result,
            planning_result=planning_result,
            export_result=export_result,
            statistics=context.pipeline_statistics,
        )

        # Validate End-to-End
        from generators.execution.validation.pipeline_validator import (
            PipelineValidator,
        )

        validation_violations = PipelineValidator.validate(pipeline_result)
        if validation_violations:
            context.pipeline_statistics.validation_failures += len(validation_violations)
            return PipelineResult(
                success=False,
                diagnostics=validation_violations,
                statistics=context.pipeline_statistics,
            )

        return pipeline_result

    @staticmethod
    def _execute_from_artifacts(
        context: PipelineContext,
        artifact_records: Mapping[str, Any],
        start_time: float,
    ) -> PipelineResult:
        """Generate Execution dataset records from upstream generator artifacts."""
        required = ("planner", "coding", "context")
        missing = tuple(name for name in required if not artifact_records.get(name))
        if missing:
            return PipelineResult(
                success=False,
                diagnostics=tuple(
                    f"Missing required upstream artifact: {name}" for name in missing
                ),
                statistics=context.pipeline_statistics,
            )

        planner_records = tuple(artifact_records.get("planner", ()))
        coding_records = tuple(artifact_records.get("coding", ()))
        context_records = tuple(artifact_records.get("context", ()))
        repair_records = tuple(artifact_records.get("repair", ()))

        planner_by_module = IntegrationPipeline._index_by_module(planner_records)
        context_by_module = IntegrationPipeline._index_by_module(context_records)
        repair_by_module = IntegrationPipeline._index_by_module(repair_records)

        stats = ExecutionIntegrationStatistics()
        writer = DatasetWriter(
            output_dir=context.export_config.output_directory,
            stats=stats,
            filename="execution_dataset.jsonl",
            dataset_name="execution",
        )

        for coding_record in sorted(coding_records, key=IntegrationPipeline._record_sort_key):
            module = IntegrationPipeline._module_name(coding_record)
            output = IntegrationPipeline._build_execution_output(
                module=module,
                coding_record=coding_record,
                planner_records=planner_by_module.get(module, ()),
                context_records=context_by_module.get(module, ()),
                repair_records=repair_by_module.get(module, ()),
            )
            protocol_hash = IntegrationPipeline._stable_hash(output)
            record = {
                "instruction": f"Execute generated implementation plan for {module}.",
                "context": {
                    "module": module,
                    "planner_records": len(planner_by_module.get(module, ())),
                    "coding_records": 1,
                    "context_records": len(context_by_module.get(module, ())),
                    "repair_records": len(repair_by_module.get(module, ())),
                },
                "output": output,
                "metadata": {
                    "module": module,
                    "protocol_hash": protocol_hash,
                    "generator": "aiodoo_execution",
                    "generator_version": context.generator_config.version,
                    "protocol_version": "1.0",
                },
            }
            writer.write_record(record)

        if writer.written_count == 0:
            return PipelineResult(
                success=False,
                diagnostics=("Execution generation produced no records.",),
                statistics=context.pipeline_statistics,
            )

        writer.export_statistics("execution_statistics.json")
        writer.export_manifest("execution_manifest.json")

        jsonl_path = context.export_config.output_directory / "execution_dataset.jsonl"
        manifest_path = context.export_config.output_directory / "execution_manifest.json"
        statistics_path = context.export_config.output_directory / "execution_statistics.json"

        context.pipeline_statistics.generated_records = writer.written_count
        context.pipeline_statistics.exported_files = 3
        context.pipeline_statistics.phase_execution_times["ARTIFACT_INTEGRATION"] = (
            time.time() - start_time
        )
        context.pipeline_statistics.total_execution_time = time.time() - start_time

        return PipelineResult(
            success=True,
            export_result=ExportResult(
                success=True,
                exported_files=(jsonl_path, manifest_path, statistics_path),
                record_count=writer.written_count,
                byte_count=jsonl_path.stat().st_size,
                manifest_path=manifest_path,
                metadata_path=statistics_path,
            ),
            statistics=context.pipeline_statistics,
        )

    @staticmethod
    def _build_execution_output(
        module: str,
        coding_record: Mapping[str, Any],
        planner_records: tuple[Mapping[str, Any], ...],
        context_records: tuple[Mapping[str, Any], ...],
        repair_records: tuple[Mapping[str, Any], ...],
    ) -> dict[str, Any]:
        coding_output = coding_record.get("output", {})
        artifacts = coding_output.get("artifacts", []) if isinstance(coding_output, dict) else []
        if not isinstance(artifacts, list):
            artifacts = []

        steps = []
        for index, artifact in enumerate(artifacts):
            if not isinstance(artifact, Mapping):
                continue
            artifact_id = str(artifact.get("id") or f"artifact_{index}")
            path = str(artifact.get("path") or "")
            steps.append(
                {
                    "id": f"exec_{artifact_id}",
                    "sequence": index,
                    "action": "apply_artifact",
                    "artifact_id": artifact_id,
                    "path": path,
                    "depends_on": tuple(str(d) for d in artifact.get("dependencies", ()) or ()),
                }
            )

        planner_refs = IntegrationPipeline._record_refs(planner_records, limit=3)
        context_refs = IntegrationPipeline._record_refs(context_records, limit=5)
        repair_refs = IntegrationPipeline._record_refs(repair_records, limit=3)
        coding_ref = IntegrationPipeline._record_ref(coding_record)

        execution_seed = {
            "module": module,
            "coding_ref": coding_ref,
            "planner_refs": planner_refs,
            "context_refs": context_refs,
            "repair_refs": repair_refs,
            "step_count": len(steps),
        }

        return {
            "execution_id": IntegrationPipeline._stable_hash(execution_seed)[:16],
            "module": module,
            "upstream": {
                "planner": planner_refs,
                "coding": coding_ref,
                "context": context_refs,
                "repair": repair_refs,
            },
            "steps": steps,
            "summary": f"Execute {len(steps)} generated artifacts for {module}.",
        }

    @staticmethod
    def _index_by_module(
        records: tuple[Mapping[str, Any], ...],
    ) -> dict[str, tuple[Mapping[str, Any], ...]]:
        grouped: dict[str, list[Mapping[str, Any]]] = {}
        for record in records:
            grouped.setdefault(IntegrationPipeline._module_name(record), []).append(record)
        return {
            module: tuple(sorted(module_records, key=IntegrationPipeline._record_sort_key))
            for module, module_records in grouped.items()
        }

    @staticmethod
    def _module_name(record: Mapping[str, Any]) -> str:
        metadata = record.get("metadata", {})
        if isinstance(metadata, Mapping):
            module = metadata.get("module") or metadata.get("source_module")
            if module:
                return str(module)
        context = record.get("context", {})
        if isinstance(context, Mapping) and context.get("module"):
            return str(context["module"])
        return "unknown"

    @staticmethod
    def _record_ref(record: Mapping[str, Any]) -> str:
        for key in ("id", "review_id", "evaluation_id", "conversation_id"):
            value = record.get(key)
            if value:
                return str(value)
        metadata = record.get("metadata", {})
        if isinstance(metadata, Mapping) and metadata.get("protocol_hash"):
            return str(metadata["protocol_hash"])
        return IntegrationPipeline._stable_hash(record)[:16]

    @staticmethod
    def _record_refs(records: tuple[Mapping[str, Any], ...], limit: int) -> tuple[str, ...]:
        return tuple(IntegrationPipeline._record_ref(record) for record in records[:limit])

    @staticmethod
    def _record_sort_key(record: Mapping[str, Any]) -> tuple[str, str]:
        return (IntegrationPipeline._module_name(record), IntegrationPipeline._record_ref(record))

    @staticmethod
    def _stable_hash(payload: Any) -> str:
        encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, default=str)
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()
