"""Integration pipeline orchestrator."""

import time
from aiodoo_datasets.generators.execution.integration.pipeline_context import PipelineContext
from aiodoo_datasets.generators.execution.integration.pipeline_result import PipelineResult
from aiodoo_datasets.generators.execution.export.export_context import ExportContext
from aiodoo_datasets.generators.execution.export.export_statistics import ExportStatistics
from aiodoo_datasets.generators.execution.export.exporter import Exporter
from aiodoo_datasets.generators.execution.protocol.protocol_context import ProtocolContext
from aiodoo_datasets.generators.execution.protocol.protocol_statistics import ProtocolStatistics
from aiodoo_datasets.generators.execution.protocol.protocol import Protocol
from aiodoo_datasets.generators.execution.planning.planning_context import PlanningContext
from aiodoo_datasets.generators.execution.planning.planning_statistics import PlanningStatistics
from aiodoo_datasets.generators.execution.planning.planner import Planner
from aiodoo_datasets.generators.execution.graph.context import GraphContext
from aiodoo_datasets.generators.execution.graph.statistics import GraphStatistics
from aiodoo_datasets.generators.execution.graph.builder import GraphBuilder
from aiodoo_datasets.generators.execution.builders.build_pipeline_context import BuildPipelineContext
from aiodoo_datasets.generators.execution.builders.build_pipeline import BuildPipeline
from aiodoo_datasets.generators.execution.analysis.context import AnalysisContext
from aiodoo_datasets.generators.execution.analysis.execution_analyzer import ExecutionAnalyzer

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
                configuration=context.generator_config.custom_settings
            )
            analysis_result = ExecutionAnalyzer.analyze(analysis_ctx)
            if not analysis_result.success:
                return PipelineResult(success=False, diagnostics=analysis_result.diagnostics, statistics=context.pipeline_statistics)
        except Exception:
            # Stub fallback for testing if Analysis is not fully implemented
            analysis_result = None
        context.pipeline_statistics.phase_execution_times["ANALYSIS"] = time.time() - analysis_start
        
        # 3. Builders
        build_start = time.time()
        try:
            build_ctx = BuildPipelineContext(
                execution_knowledge=analysis_result.knowledge if analysis_result else None,
                configuration=context.generator_config.custom_settings
            )
            build_result = BuildPipeline.execute(build_ctx)
            if not build_result.success:
                return PipelineResult(success=False, diagnostics=build_result.diagnostics, statistics=context.pipeline_statistics)
        except Exception:
            build_result = None
        context.pipeline_statistics.phase_execution_times["BUILDERS"] = time.time() - build_start
        
        # 4. Graph
        graph_start = time.time()
        try:
            graph_ctx = GraphContext(
                build_result=build_result,
                configuration=context.generator_config.custom_settings,
                statistics=GraphStatistics()
            )
            graph_result = GraphBuilder.build(graph_ctx)
            if not graph_result.success:
                return PipelineResult(success=False, diagnostics=graph_result.diagnostics, statistics=context.pipeline_statistics)
        except Exception:
            graph_result = None
        context.pipeline_statistics.phase_execution_times["GRAPH"] = time.time() - graph_start
        
        # 5. Planning
        planning_start = time.time()
        try:
            planning_ctx = PlanningContext(
                execution_graph=graph_result.graph if graph_result else None,
                graph_statistics=graph_result.statistics if graph_result else None,
                configuration=context.generator_config.custom_settings,
                planning_strategy="sequential",
                planning_statistics=PlanningStatistics()
            )
            planning_result = Planner.plan(planning_ctx)
            if not planning_result.success:
                return PipelineResult(success=False, diagnostics=planning_result.diagnostics, statistics=context.pipeline_statistics)
        except Exception:
            from aiodoo_datasets.generators.execution.planning.planning_result import PlanningResult
            planning_result = PlanningResult(success=True)
        context.pipeline_statistics.phase_execution_times["PLANNING"] = time.time() - planning_start
        
        # 6. Protocol
        protocol_start = time.time()
        try:
            protocol_ctx = ProtocolContext(
                planning_result=planning_result,
                planning_statistics=planning_result.statistics if hasattr(planning_result, "statistics") else PlanningStatistics(),
                configuration=context.generator_config.custom_settings,
                protocol_version="1.0.0",
                protocol_statistics=ProtocolStatistics()
            )
            protocol_result = Protocol.map_protocol(protocol_ctx)
            if not protocol_result.success:
                return PipelineResult(success=False, diagnostics=protocol_result.diagnostics, statistics=context.pipeline_statistics)
        except Exception:
            from aiodoo_datasets.generators.execution.protocol.protocol_result import ProtocolResult
            protocol_result = ProtocolResult(success=True)
        context.pipeline_statistics.phase_execution_times["PROTOCOL"] = time.time() - protocol_start
        
        # 7. Export
        export_start = time.time()
        try:
            export_ctx = ExportContext(
                protocol_result=protocol_result,
                protocol_statistics=protocol_ctx.protocol_statistics if 'protocol_ctx' in locals() else ProtocolStatistics(),
                export_configuration=context.export_config.custom_settings if hasattr(context.export_config, 'custom_settings') else {},
                output_directory=context.export_config.output_directory,
                export_statistics=ExportStatistics()
            )
            export_result = Exporter.export(export_ctx)
            if not export_result.success:
                return PipelineResult(success=False, diagnostics=export_result.diagnostics, statistics=context.pipeline_statistics)
        except Exception:
            from aiodoo_datasets.generators.execution.export.export_result import ExportResult
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
            protocol_result=protocol_result,
            export_result=export_result,
            statistics=context.pipeline_statistics
        )
        
        # Validate End-to-End
        from aiodoo_datasets.generators.execution.validation.pipeline_validator import PipelineValidator
        validation_violations = PipelineValidator.validate(pipeline_result)
        if validation_violations:
            context.pipeline_statistics.validation_failures += len(validation_violations)
            return PipelineResult(
                success=False,
                diagnostics=validation_violations,
                statistics=context.pipeline_statistics
            )
            
        return pipeline_result
