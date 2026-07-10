from aiodoo_datasets.generators.execution.builders.base import BaseBuilder
from aiodoo_datasets.generators.execution.builders.builder_context import BuilderContext
from aiodoo_datasets.generators.execution.builders.results.dependency_build_result import DependencyBuildResult
from aiodoo_datasets.generators.execution.analysis.knowledge.dependency_knowledge import DependencyKnowledge
from aiodoo_datasets.generators.execution.domain.execution_dependency import ExecutionDependency
from aiodoo_datasets.generators.execution.builders.operation_builder import OperationBuilder

class DependencyBuilder(BaseBuilder):
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
            diagnostics=context.diagnostics if hasattr(context, 'diagnostics') else None,
            statistics=context.statistics,
            dependencies=()
        )
