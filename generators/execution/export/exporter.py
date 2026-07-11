"""Export pipeline orchestrator."""

import time
from aiodoo_datasets.generators.execution.export.export_context import ExportContext
from aiodoo_datasets.generators.execution.export.export_result import ExportResult
from aiodoo_datasets.generators.execution.export.writers.jsonl_writer import JSONLWriter
from aiodoo_datasets.generators.execution.export.writers.manifest_writer import ManifestWriter
from aiodoo_datasets.generators.execution.export.writers.metadata_writer import MetadataWriter
from aiodoo_datasets.generators.execution.export.hooks.before_export import BeforeExportHook
from aiodoo_datasets.generators.execution.export.hooks.after_export import AfterExportHook


class Exporter:
    """
    Orchestrates the export pipeline:
    Validated Protocol -> Export Validation -> JSONL Writer -> Manifest Writer -> Metadata Writer
    """

    @staticmethod
    def export(context: ExportContext) -> ExportResult:
        """Execute the export pipeline."""
        start_time = time.time()

        from aiodoo_datasets.generators.execution.validation.export_validator import ExportValidator

        # 1. Validate
        violations = ExportValidator.validate(context)
        if violations:
            return ExportResult(
                success=False, diagnostics=violations, statistics=context.export_statistics
            )

        protocol = context.protocol_result.protocol
        plan_id = protocol.plan_id if protocol else "unknown"

        # Paths
        jsonl_path = context.output_directory / f"{plan_id}.jsonl"
        manifest_path = context.output_directory / "manifest.json"
        metadata_path = context.output_directory / "metadata.json"

        exported_files = []

        try:
            # 2. Before Hook
            BeforeExportHook.execute(context)

            # 3. Writers
            JSONLWriter().write(jsonl_path, context)
            exported_files.append(jsonl_path)

            ManifestWriter().write(manifest_path, context)
            exported_files.append(manifest_path)

            MetadataWriter().write(metadata_path, context)
            exported_files.append(metadata_path)

            # 4. After Hook
            AfterExportHook.execute(context)

        except Exception as e:
            return ExportResult(
                success=False,
                exported_files=tuple(exported_files),
                diagnostics=(f"Export failed: {e}",),
                statistics=context.export_statistics,
            )

        context.export_statistics.export_duration = time.time() - start_time

        return ExportResult(
            success=True,
            exported_files=tuple(exported_files),
            record_count=context.export_statistics.jsonl_records,
            byte_count=context.export_statistics.exported_bytes,
            manifest_path=manifest_path,
            metadata_path=metadata_path,
            statistics=context.export_statistics,
        )
