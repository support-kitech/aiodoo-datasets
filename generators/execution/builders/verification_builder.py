from aiodoo_datasets.generators.execution.builders.base import BaseBuilder
from aiodoo_datasets.generators.execution.builders.builder_context import BuilderContext
from aiodoo_datasets.generators.execution.builders.results.verification_build_result import VerificationBuildResult
from aiodoo_datasets.generators.execution.analysis.knowledge.verification_knowledge import VerificationKnowledge
from aiodoo_datasets.generators.execution.domain.execution_verification import ExecutionVerification
from aiodoo_datasets.generators.execution.builders.operation_builder import OperationBuilder

class VerificationBuilder(BaseBuilder):
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
            diagnostics=context.diagnostics if hasattr(context, 'diagnostics') else None,
            statistics=context.statistics,
            verifications=()
        )
