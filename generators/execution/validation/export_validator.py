"""Export validator orchestrator."""

from aiodoo_datasets.generators.execution.export.export_context import ExportContext
from aiodoo_datasets.generators.execution.validation.jsonl_validator import JSONLValidator
from aiodoo_datasets.generators.execution.validation.manifest_validator import ManifestValidator
from aiodoo_datasets.generators.execution.validation.metadata_validator import MetadataValidator


class ExportValidator:
    """Orchestrates validation before export begins."""

    @staticmethod
    def validate(context: ExportContext) -> tuple[str, ...]:
        """Validate context for all writers."""
        context.export_statistics.validation_execution_count += 1

        violations = []
        violations.extend(JSONLValidator.validate(context))
        violations.extend(ManifestValidator.validate(context))
        violations.extend(MetadataValidator.validate(context))

        return tuple(violations)
