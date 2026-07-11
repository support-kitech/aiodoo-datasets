"""ValidationManager public facade."""

from pathlib import Path
from typing import Any

from validation.builders.context_builder import ContextBuilder
from validation.builders.rule_builder import RuleBuilder
from validation.builders.schema_builder import SchemaBuilder
from validation.domain.results import ValidationResult
from validation.pipeline.pipeline import ValidationPipeline
from validation.pipeline.pipeline_context import PipelineContext
from validation.pipeline.pipeline_options import ValidationOptions
from validation.pipeline.pipeline_result import PipelineResult
from validation.rules.registry import RuleRegistry
from validation.schemas.registry import SchemaRegistry
from validation.validators.dataset_validator import DatasetValidator
from validation.validators.record_validator import RecordValidator


class ValidationManager:
    """
    Public facade for the Validation Framework.

    Mirrors the design of ProtocolManager and PreprocessingManager.
    Contains zero business logic — delegates to pipeline, validators, and registries.
    """

    def __init__(
        self,
        registry: RuleRegistry | None = None,
        schema_registry: SchemaRegistry | None = None,
    ) -> None:
        self._registry = registry or RuleBuilder.build_default()
        if not self._registry.is_frozen:
            self._registry.freeze()

        self._schema_registry = schema_registry or SchemaBuilder.build_default()
        if not self._schema_registry.is_frozen:
            self._schema_registry.freeze()

        self._pipeline = ValidationPipeline()

    # ---------------------------------------------------------------
    # Primary APIs
    # ---------------------------------------------------------------

    def validate(
        self,
        dataset_dir: Path,
        options: ValidationOptions | None = None,
        protocol_context: object | None = None,
    ) -> PipelineResult:
        """
        Validate all datasets in the given directory.

        Args:
            dataset_dir: Path to the datasets/ directory.
            options: Execution options (fail_fast, parallel, etc.)
            protocol_context: Optional ProtocolContext reference.

        Returns:
            PipelineResult containing the full validation report.
        """
        opts = options or ValidationOptions()
        val_context = ContextBuilder.build(dataset_dir, protocol_context)
        pipeline_context = PipelineContext(
            validation_context=val_context,
            options=opts,
            registry=self._registry,
            schema_registry=self._schema_registry,
        )
        return self._pipeline.execute(pipeline_context)

    def validate_file(
        self, jsonl_path: Path, options: ValidationOptions | None = None
    ) -> ValidationResult:
        """Validate a single JSONL file."""
        opts = options or ValidationOptions()
        val_context = ContextBuilder.build(jsonl_path.parent)
        dataset_name = jsonl_path.name
        rules = self._registry.get_rules_for_dataset(dataset_name)
        schema = self._schema_registry.resolve_from_filename(dataset_name)
        return DatasetValidator.validate(
            jsonl_path=jsonl_path,
            rules=rules,
            context=val_context,
            max_issues=opts.max_issues_per_dataset,
            schema=schema,
        )

    def validate_record(
        self, record: dict, dataset_name: str = ""  # type: ignore[type-arg]
    ) -> ValidationResult:
        """Validate a single deserialized record."""
        val_context = ContextBuilder.build(Path("."))
        rules = self._registry.get_rules_for_dataset(dataset_name)
        schema = self._schema_registry.resolve_from_filename(dataset_name)
        return RecordValidator.validate(
            record=record,
            dataset_name=dataset_name,
            record_index=0,
            rules=rules,
            context=val_context,
            schema=schema,
        )

    # ---------------------------------------------------------------
    # Extended APIs (Issue 2 — framework object validation)
    # ---------------------------------------------------------------

    def validate_generator_output(
        self, records: list[dict], generator_name: str  # type: ignore[type-arg]
    ) -> ValidationResult:
        """
        Validate a list of generator output records before export.

        Args:
            records: List of deserialized record dicts.
            generator_name: Name of the generator (e.g., "planner").

        Returns:
            Merged ValidationResult for all records.
        """
        val_context = ContextBuilder.build(Path("."))
        dataset_name = f"{generator_name}_synthetic.jsonl"
        rules = self._registry.get_rules_for_dataset(dataset_name)
        schema = self._schema_registry.get(generator_name)

        merged = ValidationResult.success(dataset_name=dataset_name)
        for idx, record in enumerate(records):
            result = RecordValidator.validate(
                record=record,
                dataset_name=dataset_name,
                record_index=idx,
                rules=rules,
                context=val_context,
                schema=schema,
            )
            merged = merged.merge(result)
        return merged

    def validate_export(
        self,
        dataset_dir: Path,
        options: ValidationOptions | None = None,
    ) -> PipelineResult:
        """
        Full export readiness validation.

        Identical to validate() but enforces all stages.
        """
        opts = options or ValidationOptions(
            validate_schemas=True,
            validate_datasets=True,
            validate_manifests=True,
            validate_cross_dataset=True,
        )
        return self.validate(dataset_dir, opts)

    def validate_repository_context(self, context: object) -> ValidationResult:
        """Structural validation of a RepositoryContext object."""
        if context is None:
            return ValidationResult.failure(
                _structural_issue("Repository context is None"),
                dataset_name="repository_context",
            )
        if not hasattr(context, "repositories"):
            return ValidationResult.failure(
                _structural_issue("Missing 'repositories' attribute"),
                dataset_name="repository_context",
            )
        return ValidationResult.success(dataset_name="repository_context")

    def validate_preprocessed_context(self, context: object) -> ValidationResult:
        """Structural validation of a PreprocessedRepositoryContext object."""
        if context is None:
            return ValidationResult.failure(
                _structural_issue("Preprocessed context is None"),
                dataset_name="preprocessed_context",
            )
        if not hasattr(context, "repositories"):
            return ValidationResult.failure(
                _structural_issue("Missing 'repositories' attribute"),
                dataset_name="preprocessed_context",
            )
        return ValidationResult.success(dataset_name="preprocessed_context")

    def validate_protocol_context(self, context: object) -> ValidationResult:
        """Structural validation of a ProtocolContext object."""
        if context is None:
            return ValidationResult.failure(
                _structural_issue("Protocol context is None"),
                dataset_name="protocol_context",
            )
        if not hasattr(context, "dataset"):
            return ValidationResult.failure(
                _structural_issue("Missing 'dataset' attribute"),
                dataset_name="protocol_context",
            )
        return ValidationResult.success(dataset_name="protocol_context")

    # ---------------------------------------------------------------
    # Introspection
    # ---------------------------------------------------------------

    def summary(self) -> dict[str, Any]:
        """Return a summary of the validation framework state."""
        from validation.constants.framework import VALIDATION_FRAMEWORK_VERSION

        return {
            "framework_version": VALIDATION_FRAMEWORK_VERSION,
            "registry_hash": self._registry.hash_value,
            "schema_registry_hash": self._schema_registry.hash_value,
            "total_rules": len(self._registry.all_rules),
            "total_schemas": len(self._schema_registry.all_schemas),
            "rule_ids": [r.rule_id for r in self._registry.all_rules],
            "schema_ids": [s.schema_id for s in self._schema_registry.all_schemas],
        }


def _structural_issue(message: str) -> "ValidationIssue":  # noqa: F821
    """Create a structural validation issue."""
    from validation.domain.enums import ValidationSeverity, ValidationCategory
    from validation.domain.models import ValidationIssue

    return ValidationIssue(
        rule_id="STRUCT-001",
        severity=ValidationSeverity.FATAL,
        category=ValidationCategory.SCHEMA,
        message=message,
        dataset_name="framework",
    )
