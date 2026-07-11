from generators.execution.builders.base import BaseBuilder
from generators.execution.builders.builder_context import BuilderContext
from generators.execution.builders.results.verification_build_result import (
    VerificationBuildResult,
)
from generators.execution.analysis.knowledge.verification_knowledge import (
    VerificationKnowledge,
)
from generators.execution.domain.execution_verification import ExecutionVerification
from generators.execution.builders.operation_builder import OperationBuilder


class VerificationBuilder(BaseBuilder):  # type: ignore[misc]
    PRIORITY = 50
    REQUIRES = (OperationBuilder,)
    INPUT = VerificationKnowledge
    OUTPUT = ExecutionVerification

    def build(self, context: BuilderContext) -> VerificationBuildResult:
        return VerificationBuildResult(
            builder_name=self.__class__.__name__,
            builder_version="1.0.0",
            execution_time=0.0,
            success=True,
            diagnostics=context.diagnostics if hasattr(context, "diagnostics") else None,
            statistics=context.statistics,
            verifications=(),
        )
