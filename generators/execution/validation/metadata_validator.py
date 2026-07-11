"""Validator for metadata export context."""

from generators.execution.export.export_context import ExportContext


class MetadataValidator:
    """Validates that the context is ready for Metadata export."""

    @staticmethod
    def validate(context: ExportContext) -> tuple[str, ...]:
        violations = []
        if not context.protocol_result.protocol:
            violations.append("Cannot write metadata: Protocol domain object is missing.")
        return tuple(violations)
