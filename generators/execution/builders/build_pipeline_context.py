from dataclasses import dataclass
from typing import Any
from generators.execution.builders.builder_context import BuilderContext
from generators.execution.builders.diagnostics.builder_diagnostics import (
    BuilderDiagnostics,
)


@dataclass(frozen=True, slots=True)
class BuildPipelineContext:
    """
    The master orchestration context.
    It holds the domain context, the registries, and the pipeline-level diagnostics.
    """

    builder_context: BuilderContext
    builder_registry: Any  # Type hinted as Any to avoid circular import during orchestration setup
    factory_registry: Any
    diagnostics: BuilderDiagnostics
