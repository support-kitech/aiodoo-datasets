from types import MappingProxyType
from aiodoo_datasets.generators.execution.builders.base import BaseBuilder
from aiodoo_datasets.generators.execution.builders.builder_context import BuilderContext
from aiodoo_datasets.generators.execution.builders.results.metadata_build_result import (
    MetadataBuildResult,
)
from aiodoo_datasets.generators.execution.builders.operation_builder import OperationBuilder


class MetadataBuilder(BaseBuilder):
    PRIORITY = 70
    REQUIRES = (OperationBuilder,)
    INPUT = dict
    OUTPUT = MappingProxyType

    def build(self, context: BuilderContext) -> MetadataBuildResult:
        return MetadataBuildResult(
            builder_name=self.__class__.__name__,
            builder_version="1.0.0",
            execution_time=0.0,
            success=True,
            diagnostics=context.diagnostics if hasattr(context, "diagnostics") else None,
            statistics=context.statistics,
            metadata=MappingProxyType({}),
        )
