"""Assembly pipeline for the Protocol Framework."""

import time

from protocol.builders.base import IdentifierFactory
from protocol.builders.context_builder import ContextBuilder
from protocol.builders.dataset_builder import DatasetBuilder
from protocol.builders.manifest_builder import ManifestBuilder
from protocol.builders.metadata_builder import MetadataBuilder
from protocol.builders.reference_builder import ReferenceBuilder
from protocol.builders.schema_builder import SchemaBuilder
from protocol.domain.enums import ExportFormat, ReferenceType
from protocol.domain.version import ProtocolVersion
from protocol.pipeline.pipeline_context import PipelineContext
from protocol.pipeline.pipeline_result import PipelineResult
from protocol.pipeline.pipeline_statistics import PipelineStatistics
from protocol.serialization.exporter import Exporter
from protocol.validation.dataset_validator import DatasetValidator


class AssemblyPipeline:
    """
    Coordinates the construction, validation, and export of protocol graphs.

    Does not contain business logic. Delegates construction to Builders,
    verification to Validators, and output generation to Exporters.
    """

    def assemble(self, context: PipelineContext) -> PipelineResult:
        """
        Assemble the final ProtocolContext from the input context.
        """
        start_time = time.perf_counter()

        # In a real implementation, these properties would be mapped precisely
        # from the input_context (e.g. PreprocessedRepositoryContext).
        # We extract what we can dynamically to remain loosely coupled.
        input_ctx = context.input_context

        # Extract metadata properties if available, else empty dict
        meta_props = getattr(input_ctx, "metadata", {})
        if not isinstance(meta_props, dict):
            meta_props = {}

        # 1. Builders
        # Build Version
        version = ProtocolVersion(
            identifier=IdentifierFactory.for_version("default"),
            framework_version="1.0.0",
            schema_version="1.0.0",
            generator_version="1.0.0",
        )

        # Build Metadata
        metadata = MetadataBuilder.build(meta_props)

        # Build Repository Reference
        repo_name = getattr(input_ctx, "name", "unknown_repository")
        repo_ref = ReferenceBuilder.build(ReferenceType.REPOSITORY, repo_name)

        # Build Manifest
        manifest = ManifestBuilder.build(
            version=version,
            metadata=metadata,
            repository_reference=repo_ref,
        )

        # Build Schema
        schema = SchemaBuilder.build("1.0.0")

        # Build Dataset
        dataset = DatasetBuilder.build(manifest=manifest, schema=schema)

        # Build Protocol Context
        protocol_context = ContextBuilder.build(dataset)

        assembly_time_ms = (time.perf_counter() - start_time) * 1000

        # 2. Validation
        if context.options.validate_schema:
            validation_result = DatasetValidator.validate(dataset)
            if not validation_result.valid:
                return PipelineResult(
                    protocol_context=None,
                    validation_result=validation_result,
                    statistics=PipelineStatistics(
                        objects_created=1,
                        validation_count=1,
                        assembly_duration_ms=assembly_time_ms,
                    ),
                    export_payload=None,
                )
        else:
            validation_result = DatasetValidator.validate(dataset) # Still validate structurally but maybe ignore?
            # For structural validation we always validate
            validation_result = DatasetValidator.validate(dataset)

        # 3. Export
        export_start = time.perf_counter()
        export_payload = None
        if context.options.export_format:
            fmt_enum = ExportFormat(context.options.export_format.lower())
            export_payload = Exporter.export(protocol_context, fmt=fmt_enum)

        export_time_ms = (time.perf_counter() - export_start) * 1000

        statistics = PipelineStatistics(
            objects_created=7,  # Version, Metadata, Ref, Manifest, Schema, Dataset, Context
            relationships_created=0,
            references_created=1,
            validation_count=1,
            serialization_count=1 if export_payload else 0,
            assembly_duration_ms=assembly_time_ms,
            validation_duration_ms=0.0, # TODO: Track properly
            serialization_duration_ms=export_time_ms if export_payload else 0.0,
            export_duration_ms=export_time_ms,
        )

        return PipelineResult(
            protocol_context=protocol_context,
            validation_result=validation_result,
            statistics=statistics,
            export_payload=export_payload,
        )
