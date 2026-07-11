"""Manager for the Protocol Framework."""

from typing import Any

from protocol.domain.dataset import ProtocolContext
from protocol.domain.enums import ExportFormat
from protocol.pipeline.assembly_options import AssemblyOptions
from protocol.pipeline.pipeline import AssemblyPipeline
from protocol.pipeline.pipeline_context import PipelineContext
from protocol.pipeline.pipeline_result import PipelineResult
from protocol.registry.registry import ProtocolRegistry


class ProtocolManager:
    """
    Thin façade for the Protocol Framework.
    Delegates entirely to AssemblyPipeline.
    """

    def __init__(self, registry: ProtocolRegistry | None = None) -> None:
        self.registry = registry or ProtocolRegistry()
        if not self.registry.is_frozen:
            self.registry.freeze()
        self.pipeline = AssemblyPipeline()

    def assemble(
        self, input_context: Any, options: AssemblyOptions | None = None
    ) -> PipelineResult:
        """
        Assemble a ProtocolContext from an input context.
        """
        opts = options or AssemblyOptions()
        ctx = PipelineContext(
            input_context=input_context,
            options=opts,
            registry=self.registry,
        )
        return self.pipeline.assemble(ctx)

    def export(
        self, context: ProtocolContext, fmt: ExportFormat = ExportFormat.JSON
    ) -> str | dict[str, Any]:
        """
        Export a ProtocolContext to the specified format.
        """
        from protocol.serialization.exporter import Exporter

        return Exporter.export(context, fmt=fmt)

    def validate(self, context: ProtocolContext) -> Any:
        """
        Validate a ProtocolContext structurally.
        """
        from protocol.validation.dataset_validator import DatasetValidator

        return DatasetValidator.validate(context.dataset)

    def summary(self) -> dict[str, Any]:
        """
        Return a summary of the protocol framework and registry state.
        """
        from protocol.constants.framework import PROTOCOL_FRAMEWORK_VERSION, SERIALIZER_VERSION

        return {
            "framework_version": PROTOCOL_FRAMEWORK_VERSION,
            "serializer_version": SERIALIZER_VERSION,
            "registry_hash": self.registry.hash_value,
            "protocol_types_count": len(self.registry.protocol_types),
            "schema_versions_count": len(self.registry.schema_versions),
            "relationship_types_count": len(self.registry.relationship_types),
            "export_formats": list(self.registry.export_formats.keys()),
        }
