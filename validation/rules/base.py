"""Base rule abstraction for the Validation Framework."""

import abc

from validation.constants.framework import SCHEMA_RULE_PRIORITY
from validation.domain.enums import (
    ValidationSeverity,
    ValidationCategory,
    RuleScope,
)
from validation.domain.models import ValidationIssue, ValidationContext


class BaseRule(abc.ABC):
    """
    Abstract base class for all validation rules.

    Rules are stateless and pure. They receive a single deserialized
    record dict and return zero or more ValidationIssue objects.
    """

    @property
    @abc.abstractmethod
    def rule_id(self) -> str:
        """Globally unique, stable identifier (e.g. 'SCH-001')."""

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """Human-readable description of what this rule checks."""

    @property
    @abc.abstractmethod
    def severity(self) -> ValidationSeverity:
        """Default severity for issues produced by this rule."""

    @property
    @abc.abstractmethod
    def category(self) -> ValidationCategory:
        """Category this rule belongs to."""

    @property
    def priority(self) -> int:
        """Execution priority. Lower numbers execute first."""
        return SCHEMA_RULE_PRIORITY

    @property
    def scope(self) -> RuleScope:
        """Whether this rule applies universally or to specific generators."""
        return RuleScope.UNIVERSAL

    @property
    def target_generators(self) -> tuple[str, ...]:
        """Generator names this rule applies to. Empty tuple means all generators."""
        return ()

    @property
    def enabled(self) -> bool:
        """Whether this rule is active."""
        return True

    @abc.abstractmethod
    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        """
        Validate a single deserialized record.

        Args:
            record: A deserialized JSONL record (dict).
            context: The immutable validation context.

        Returns:
            A tuple of zero or more ValidationIssue objects.
        """

    def _issue(
        self,
        message: str,
        dataset_name: str,
        record_index: int | None = None,
        field_path: str = "",
    ) -> ValidationIssue:
        """Helper to create an issue with this rule's defaults."""
        return ValidationIssue(
            rule_id=self.rule_id,
            severity=self.severity,
            category=self.category,
            message=message,
            dataset_name=dataset_name,
            record_index=record_index,
            field_path=field_path,
        )
