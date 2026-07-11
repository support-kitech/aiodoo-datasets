"""Validator for manifest export context."""

from aiodoo_datasets.generators.execution.export.export_context import ExportContext


class ManifestValidator:
    """Validates that the context is ready for Manifest export."""

    @staticmethod
    def validate(context: ExportContext) -> tuple[str, ...]:
        violations = []
        if not context.protocol_result.protocol:
            violations.append("Cannot write manifest: Protocol domain object is missing.")
        return tuple(violations)
