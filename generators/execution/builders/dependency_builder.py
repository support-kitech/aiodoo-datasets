from generators.execution.builders.base import BaseBuilder
from generators.execution.builders.builder_context import BuilderContext
from generators.execution.builders.results.dependency_build_result import (
    DependencyBuildResult,
)
from generators.execution.analysis.knowledge.dependency_knowledge import (
    DependencyKnowledge,
)
from generators.execution.domain.execution_dependency import ExecutionDependency
from generators.execution.builders.operation_builder import OperationBuilder


class DependencyBuilder(BaseBuilder):  # type: ignore[misc]
    PRIORITY = 30
    REQUIRES = (OperationBuilder,)
    INPUT = DependencyKnowledge
    OUTPUT = ExecutionDependency

    def build(self, context: BuilderContext) -> DependencyBuildResult:
        return DependencyBuildResult(
            builder_name=self.__class__.__name__,
            builder_version="1.0.0",
            execution_time=0.0,
            success=True,
            diagnostics=context.diagnostics if hasattr(context, "diagnostics") else None,
            statistics=context.statistics,
            dependencies=(),
        )
