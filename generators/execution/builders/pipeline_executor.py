from types import MappingProxyType
from aiodoo_datasets.generators.execution.builders.build_pipeline_context import (
    BuildPipelineContext,
)
from aiodoo_datasets.generators.execution.builders.pipeline_result import PipelineResult


class PipelineExecutor:
    """
    Executes the stateless lifecycle of all registered Builders.
    """

    def execute(self, context: BuildPipelineContext) -> PipelineResult:
        results = {}
        failed = []
        skipped = []

        builders = context.builder_registry.items()

        for builder in builders:
            builder_name = builder.__class__.__name__
            try:
                # Lifecycle
                builder.before_build(context.builder_context)

                result = builder.build(context.builder_context)

                builder.after_build(context.builder_context, result)

                results[builder_name] = result
                if not result.success:
                    failed.append(builder_name)

            except Exception:
                failed.append(builder_name)

        return PipelineResult(
            success=len(failed) == 0,
            results=MappingProxyType(results),
            diagnostics=context.diagnostics,
            statistics=context.builder_context.statistics,
            failed_builders=tuple(failed),
            skipped_builders=tuple(skipped),
        )
