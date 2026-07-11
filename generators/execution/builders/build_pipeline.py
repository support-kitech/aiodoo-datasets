from generators.execution.builders.build_pipeline_context import (
    BuildPipelineContext,
)
from generators.execution.builders.pipeline_result import PipelineResult


class BuildPipeline:
    """
    Public API orchestrator for the Builder phase.
    Contains no business logic, iteration, or lifecycle logic itself.
    """

    def __init__(self, executor) -> None:  # type: ignore[no-untyped-def]
        self.executor = executor

    def before_pipeline(self, context: BuildPipelineContext) -> None:
        """Hook for future multiprocessing/distributed setup."""
        pass

    def after_pipeline(self, context: BuildPipelineContext, result: PipelineResult) -> None:
        """Hook for future multiprocessing/distributed teardown."""
        pass

    def execute(self, context: BuildPipelineContext) -> PipelineResult:
        """
        Executes the entire deterministic Builder pipeline.
        """
        self.before_pipeline(context)

        # Validation checks on registries before executing
        context.builder_registry.validate()
        context.factory_registry.validate()

        # Executor runs the stateless lifecycle hooks and returns results
        result = self.executor.execute(context)

        self.after_pipeline(context, result)
        return result
