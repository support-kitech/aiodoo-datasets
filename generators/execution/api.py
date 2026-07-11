"""Public API for the Execution Generator."""

from generators.execution.version import __version__
from generators.execution.integration.pipeline import (
    IntegrationPipeline as _IntegrationPipeline,
)
from generators.execution.integration.pipeline_context import (
    PipelineContext as _PipelineContext,
)
from generators.execution.integration.pipeline_result import (
    PipelineResult as _PipelineResult,
)
from generators.execution.validation.pipeline_validator import (
    PipelineValidator as _PipelineValidator,
)
from generators.execution.export.exporter import Exporter as _Exporter
from generators.execution.export.export_context import (
    ExportContext as _ExportContext,
)
from generators.execution.export.export_result import ExportResult as _ExportResult


def generate(context: _PipelineContext) -> _PipelineResult:
    """
    Execute the entire generation pipeline.

    Args:
        context: The immutable pipeline context.

    Returns:
        The pipeline result containing exported datasets and statistics.
    """
    return _IntegrationPipeline.execute(context)


def validate(result: _PipelineResult) -> tuple[str, ...]:
    """
    Validate a complete pipeline execution result.

    Args:
        result: The pipeline result.

    Returns:
        A tuple of validation violation messages. Empty if successful.
    """
    return _PipelineValidator.validate(result)  # type: ignore[no-any-return]


def export(context: _ExportContext) -> _ExportResult:
    """
    Execute only the export phase manually.

    Args:
        context: The immutable export context.

    Returns:
        The export result.
    """
    return _Exporter.export(context)


__all__ = [
    "generate",
    "validate",
    "export",
    "__version__",
]
