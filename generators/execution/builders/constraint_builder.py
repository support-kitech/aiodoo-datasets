from generators.execution.builders.base import BaseBuilder
from generators.execution.builders.builder_context import BuilderContext
from generators.execution.builders.results.constraint_build_result import (
    ConstraintBuildResult,
)
from generators.execution.analysis.knowledge.constraint_knowledge import (
    ConstraintKnowledge,
)
from generators.execution.domain.execution_constraint import ExecutionConstraint
from generators.execution.builders.operation_builder import OperationBuilder


class ConstraintBuilder(BaseBuilder):  # type: ignore[misc]
    PRIORITY = 40
    REQUIRES = (OperationBuilder,)
    INPUT = ConstraintKnowledge
    OUTPUT = ExecutionConstraint

    def build(self, context: BuilderContext) -> ConstraintBuildResult:
        return ConstraintBuildResult(
            builder_name=self.__class__.__name__,
            builder_version="1.0.0",
            execution_time=0.0,
            success=True,
            diagnostics=context.diagnostics if hasattr(context, "diagnostics") else None,
            statistics=context.statistics,
            constraints=(),
        )
