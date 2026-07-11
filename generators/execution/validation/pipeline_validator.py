"""Validator for complete pipeline execution."""

from aiodoo_datasets.generators.execution.integration.pipeline_result import PipelineResult


class PipelineValidator:
    """Validates complete pipeline execution and generated artifacts."""

    @staticmethod
    def validate(result: PipelineResult) -> tuple[str, ...]:
        violations = []

        if not result.export_result or not result.export_result.success:
            violations.append("Validation failed: Export was not successful.")
            return tuple(violations)

        if result.export_result.record_count == 0:
            violations.append("Validation failed: No records were exported.")

        if len(result.export_result.exported_files) == 0:
            violations.append("Validation failed: No files were exported.")

        # Additional deep validations could check protocol consistency, graph consistency, etc.

        return tuple(violations)
