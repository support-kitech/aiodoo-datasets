"""Public API for the Approval Generator."""

from aiodoo_datasets.generators.approval.pipeline_context import PipelineContext
from aiodoo_datasets.generators.approval.pipeline_result import PipelineResult
from aiodoo_datasets.generators.approval.pipeline import ApprovalPipeline
from aiodoo_datasets.generators.approval.protocol.version import __version__ as protocol_version


def generate(context: PipelineContext) -> PipelineResult:
    """Generate an approval review based on input protocols."""
    return ApprovalPipeline.generate(context)


def validate(context: PipelineContext) -> PipelineResult:
    """Validate without full generation (currently delegates to generate)."""
    return ApprovalPipeline.generate(context)


def export(context: PipelineContext) -> PipelineResult:
    """Export the review (implementation links to common exporter)."""
    # Exporter logic goes here, tying into common JSONLWriter
    return ApprovalPipeline.generate(context)


__all__ = ["generate", "validate", "export", "protocol_version"]
