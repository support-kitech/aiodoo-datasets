from generators.execution.builders.base import BaseBuilder
from generators.execution.builders.builder_context import BuilderContext
from generators.execution.builders.results.rollback_build_result import (
    RollbackBuildResult,
)
from generators.execution.analysis.knowledge.rollback_knowledge import (
    RollbackKnowledge,
)
from generators.execution.domain.execution_rollback import ExecutionRollback
from generators.execution.builders.operation_builder import OperationBuilder


class RollbackBuilder(BaseBuilder):  # type: ignore[misc]
    PRIORITY = 60
    REQUIRES = (OperationBuilder,)
    INPUT = RollbackKnowledge
    OUTPUT = ExecutionRollback

    def build(self, context: BuilderContext) -> RollbackBuildResult:
        return RollbackBuildResult(
            builder_name=self.__class__.__name__,
            builder_version="1.0.0",
            execution_time=0.0,
            success=True,
            diagnostics=context.diagnostics if hasattr(context, "diagnostics") else None,
            statistics=context.statistics,
            rollbacks=(),
        )
