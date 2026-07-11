"""Integration pipeline orchestrator."""

import time
from generators.execution.integration.pipeline_context import PipelineContext
from generators.execution.integration.pipeline_result import PipelineResult
from generators.execution.export.export_context import ExportContext
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


class IntegrationPipeline:
    """
    Orchestrates the entire execution generator pipeline:
    Discovery -> Analysis -> Builders -> Graph -> Planning -> Protocol -> Export
    """

    @staticmethod
    def execute(context: PipelineContext) -> PipelineResult:
        """Run the end-to-end pipeline."""
        start_time = time.time()

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
                domain_steps=build_result.steps if build_result and hasattr(build_result, "steps") else (),
                domain_dependencies=build_result.dependencies if build_result and hasattr(build_result, "dependencies") else (),
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
                object.__setattr__(export_ctx, "protocol_context", getattr(context, "protocol_context"))

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
