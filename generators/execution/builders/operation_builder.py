from aiodoo_datasets.generators.execution.builders.base import BaseBuilder
from aiodoo_datasets.generators.execution.builders.builder_context import BuilderContext
from aiodoo_datasets.generators.execution.builders.results.operation_build_result import (
    OperationBuildResult,
)
from aiodoo_datasets.generators.execution.analysis.knowledge.operation_knowledge import (
    OperationKnowledge,
)
from aiodoo_datasets.generators.execution.domain.execution_operation import ExecutionOperation
from aiodoo_datasets.generators.execution.builders.artifact_builder import ArtifactBuilder


class OperationBuilder(BaseBuilder):  # type: ignore[misc]
    PRIORITY = 20
    REQUIRES = (ArtifactBuilder,)
    INPUT = OperationKnowledge
    OUTPUT = ExecutionOperation

    def build(self, context: BuilderContext) -> OperationBuildResult:
        return OperationBuildResult(
            builder_name=self.__class__.__name__,
            builder_version="1.0.0",
            execution_time=0.0,
            success=True,
            diagnostics=context.diagnostics if hasattr(context, "diagnostics") else None,
            statistics=context.statistics,
            operations=(),
        )
