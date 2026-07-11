from aiodoo_datasets.generators.execution.builders.base import BaseBuilder
from aiodoo_datasets.generators.execution.builders.builder_context import BuilderContext
from aiodoo_datasets.generators.execution.builders.results.rollback_build_result import (
    RollbackBuildResult,
)
from aiodoo_datasets.generators.execution.analysis.knowledge.rollback_knowledge import (
    RollbackKnowledge,
)
from aiodoo_datasets.generators.execution.domain.execution_rollback import ExecutionRollback
from aiodoo_datasets.generators.execution.builders.operation_builder import OperationBuilder


class RollbackBuilder(BaseBuilder):
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
