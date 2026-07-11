from aiodoo_datasets.generators.execution.builders.base import BaseBuilder
from aiodoo_datasets.generators.execution.builders.builder_context import BuilderContext
from aiodoo_datasets.generators.execution.builders.results.artifact_build_result import (
    ArtifactBuildResult,
)
from aiodoo_datasets.generators.execution.analysis.knowledge.artifact_knowledge import (
    ArtifactKnowledge,
)
from aiodoo_datasets.generators.execution.artifacts.artifact import Artifact


class ArtifactBuilder(BaseBuilder):
    PRIORITY = 10
    REQUIRES = ()
    INPUT = ArtifactKnowledge
    OUTPUT = Artifact

    def build(self, context: BuilderContext) -> ArtifactBuildResult:
        # Business logic goes here using FactoryRegistry
        return ArtifactBuildResult(
            builder_name=self.__class__.__name__,
            builder_version="1.0.0",
            execution_time=0.0,
            success=True,
            diagnostics=context.diagnostics if hasattr(context, "diagnostics") else None,
            statistics=context.statistics,
            artifacts=(),
        )
