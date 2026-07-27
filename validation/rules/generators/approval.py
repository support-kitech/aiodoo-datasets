"""Generator-specific validation rules for the Approval dataset."""

from __future__ import annotations

import re

from validation.constants.framework import GENERATOR_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory, RuleScope
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule

# Keep in sync with generators.approval.policy.MAX_EVIDENCE_ITEMS
_MAX_EVIDENCE_ITEMS = 32
_MIN_PRODUCTION_RECORDS = 2
_RECORD_ID_RE = re.compile(r"^APR-[0-9a-f]{32}$")
_ALLOWED_CAPABILITIES = frozenset({"planner", "coding", "repair", "execution"})


class ApprovalDecisionRule(BaseRule):
    """Approval record must contain a valid decision object."""

    @property
    def rule_id(self) -> str:
        return "APR-001"

    @property
    def description(self) -> str:
        return "Approval record must contain a valid decision."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.ERROR

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.GENERATOR

    @property
    def priority(self) -> int:
        return GENERATOR_RULE_PRIORITY

    @property
    def scope(self) -> RuleScope:
        return RuleScope.GENERATOR_SPECIFIC

    @property
    def target_generators(self) -> tuple[str, ...]:
        return ("approval",)

    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        decision = record.get("decision")
        if not isinstance(decision, dict):
            return (
                self._issue(
                    message="Approval record has missing or invalid decision object",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="decision",
                ),
            )

        issues: list[ValidationIssue] = []
        for field in ("status", "decision_id"):
            if not decision.get(field):
                issues.append(
                    self._issue(
                        message=f"Decision missing required field: '{field}'",
                        dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                        record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                        field_path=f"decision.{field}",
                    )
                )
        return tuple(issues)


class ApprovalIdentityRule(BaseRule):
    """Approval records must carry stable Step 2.1 identities."""

    @property
    def rule_id(self) -> str:
        return "APR-002"

    @property
    def description(self) -> str:
        return "Approval record_id/subject identity fields must be present and well-formed."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.ERROR

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.GENERATOR

    @property
    def priority(self) -> int:
        return GENERATOR_RULE_PRIORITY + 1

    @property
    def scope(self) -> RuleScope:
        return RuleScope.GENERATOR_SPECIFIC

    @property
    def target_generators(self) -> tuple[str, ...]:
        return ("approval",)

    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        ds = context.metadata.get("current_dataset", "")
        idx = context.metadata.get("current_index")
        issues: list[ValidationIssue] = []

        record_id = record.get("record_id")
        if not isinstance(record_id, str) or not _RECORD_ID_RE.match(record_id):
            issues.append(
                self._issue(
                    message="Approval record_id must match APR-<32 hex> scheme",
                    dataset_name=ds,  # type: ignore[arg-type]
                    record_index=idx,  # type: ignore[arg-type]
                    field_path="record_id",
                )
            )

        capability = record.get("capability")
        if capability not in _ALLOWED_CAPABILITIES:
            issues.append(
                self._issue(
                    message="Approval capability must be planner|coding|repair|execution",
                    dataset_name=ds,  # type: ignore[arg-type]
                    record_index=idx,  # type: ignore[arg-type]
                    field_path="capability",
                )
            )

        for field in ("subject_id", "source_object_id", "subject"):
            value = record.get(field)
            if not isinstance(value, str) or not value.strip():
                issues.append(
                    self._issue(
                        message=f"Approval '{field}' must be a non-empty string",
                        dataset_name=ds,  # type: ignore[arg-type]
                        record_index=idx,  # type: ignore[arg-type]
                        field_path=field,
                    )
                )

        review_id = record.get("review_id")
        if isinstance(record_id, str) and isinstance(review_id, str) and review_id != record_id:
            issues.append(
                self._issue(
                    message="Approval review_id must equal record_id",
                    dataset_name=ds,  # type: ignore[arg-type]
                    record_index=idx,  # type: ignore[arg-type]
                    field_path="review_id",
                )
            )

        return tuple(issues)


class ApprovalBoundedEvidenceRule(BaseRule):
    """Evidence written into an Approval record must be bounded."""

    @property
    def rule_id(self) -> str:
        return "APR-003"

    @property
    def description(self) -> str:
        return "Approval evidence list must not exceed the production bound."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.ERROR

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.GENERATOR

    @property
    def priority(self) -> int:
        return GENERATOR_RULE_PRIORITY + 2

    @property
    def scope(self) -> RuleScope:
        return RuleScope.GENERATOR_SPECIFIC

    @property
    def target_generators(self) -> tuple[str, ...]:
        return ("approval",)

    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        evidence = record.get("evidence")
        if not isinstance(evidence, list):
            return (
                self._issue(
                    message="Approval evidence must be a list",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="evidence",
                ),
            )
        if len(evidence) > _MAX_EVIDENCE_ITEMS:
            return (
                self._issue(
                    message=(
                        f"Approval evidence length {len(evidence)} exceeds "
                        f"bound {_MAX_EVIDENCE_ITEMS}"
                    ),
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="evidence",
                ),
            )
        return ()


class ApprovalProductionScaleRule(BaseRule):
    """Reject single-record placeholder Approval datasets at finalize time."""

    def __init__(self) -> None:
        self._count = 0

    @property
    def rule_id(self) -> str:
        return "APR-004"

    @property
    def description(self) -> str:
        return "Approval production datasets must contain multiple subject decisions."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.FATAL

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.GENERATOR

    @property
    def priority(self) -> int:
        return GENERATOR_RULE_PRIORITY + 3

    @property
    def scope(self) -> RuleScope:
        return RuleScope.GENERATOR_SPECIFIC

    @property
    def target_generators(self) -> tuple[str, ...]:
        return ("approval",)

    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        self._count += 1
        return ()

    def reset(self) -> None:
        self._count = 0

    def finalize(
        self,
        *,
        dataset_name: str,
        records_validated: int,
    ) -> tuple[ValidationIssue, ...]:
        count = records_validated if records_validated else self._count
        if count < _MIN_PRODUCTION_RECORDS:
            return (
                self._issue(
                    message=(
                        f"Approval dataset has {count} record(s); "
                        f"production minimum is {_MIN_PRODUCTION_RECORDS} "
                        "(placeholder single-review grain rejected)"
                    ),
                    dataset_name=dataset_name,
                ),
            )
        return ()
