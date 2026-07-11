"""Validator for JSONL export context."""

from aiodoo_datasets.generators.execution.export.export_context import ExportContext


class JSONLValidator:
    """Validates that the context is ready for JSONL export."""

    @staticmethod
    def validate(context: ExportContext) -> tuple[str, ...]:
        violations = []
        if not context.protocol_result.success:
            violations.append("Cannot export: Protocol mapping failed.")
        if not context.protocol_result.serialized_data:
            violations.append("Cannot export: Serialized data is empty.")
        if not context.output_directory:
            violations.append("Cannot export: Output directory is missing.")

        return tuple(violations)
