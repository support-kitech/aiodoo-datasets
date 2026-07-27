"""Generator-specific validation rules for Evaluation SFT and BenchmarkCatalog."""

from __future__ import annotations

import re

from validation.constants.framework import GENERATOR_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory, RuleScope
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule

_MIN_PRODUCTION_RECORDS = 2
_RECORD_ID_RE = re.compile(r"^EVL-[0-9a-f]{32}$")
_CANDIDATE_ID_RE = re.compile(r"^CAND-[0-9a-f]{24}$")
_ALLOWED_VERDICTS = frozenset({"pass", "fail", "inconclusive"})
_ALLOWED_CASE_KEYS = frozenset({"pass", "fail", "inconclusive"})


class EvaluationCatalogRule(BaseRule):
    """BenchmarkCatalog records must contain a valid catalog object.

    Targets the separate ``benchmark_catalog`` artifact only — not Evaluation SFT.
    """

    @property
    def rule_id(self) -> str:
        return "EVL-001"

    @property
    def description(self) -> str:
        return "BenchmarkCatalog record must contain a valid catalog."

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
        return ("benchmark_catalog",)

    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        catalog = record.get("catalog")
        if not isinstance(catalog, dict):
            return (
                self._issue(
                    message="BenchmarkCatalog record has missing or invalid catalog object",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="catalog",
                ),
            )

        issues: list[ValidationIssue] = []
        for field in ("catalog_id", "catalog_name"):
            if not catalog.get(field):
                issues.append(
                    self._issue(
                        message=f"Catalog missing required field: '{field}'",
                        dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                        record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                        field_path=f"catalog.{field}",
                    )
                )
        return tuple(issues)


class EvaluationIdentityRule(BaseRule):
    """Evaluation SFT records must carry stable Step 2.1 identities."""

    @property
    def rule_id(self) -> str:
        return "EVL-002"

    @property
    def description(self) -> str:
        return "Evaluation record_id/candidate_id/case key must be well-formed."

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
        return ("evaluation",)

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
                    message="Evaluation record_id must match EVL-<32 hex> scheme",
                    dataset_name=ds,  # type: ignore[arg-type]
                    record_index=idx,  # type: ignore[arg-type]
                    field_path="record_id",
                )
            )

        candidate_id = record.get("candidate_id")
        if not isinstance(candidate_id, str) or not _CANDIDATE_ID_RE.match(candidate_id):
            issues.append(
                self._issue(
                    message="Evaluation candidate_id must match CAND-<24 hex> scheme",
                    dataset_name=ds,  # type: ignore[arg-type]
                    record_index=idx,  # type: ignore[arg-type]
                    field_path="candidate_id",
                )
            )

        case_key = record.get("evaluation_case_key")
        if case_key not in _ALLOWED_CASE_KEYS:
            issues.append(
                self._issue(
                    message="Evaluation evaluation_case_key must be pass|fail|inconclusive",
                    dataset_name=ds,  # type: ignore[arg-type]
                    record_index=idx,  # type: ignore[arg-type]
                    field_path="evaluation_case_key",
                )
            )

        verdict = record.get("verdict")
        if verdict not in _ALLOWED_VERDICTS:
            issues.append(
                self._issue(
                    message="Evaluation verdict must be pass|fail|inconclusive",
                    dataset_name=ds,  # type: ignore[arg-type]
                    record_index=idx,  # type: ignore[arg-type]
                    field_path="verdict",
                )
            )

        candidate = record.get("candidate")
        if not isinstance(candidate, dict) or not candidate:
            issues.append(
                self._issue(
                    message="Evaluation candidate must be a non-empty object",
                    dataset_name=ds,  # type: ignore[arg-type]
                    record_index=idx,  # type: ignore[arg-type]
                    field_path="candidate",
                )
            )

        return tuple(issues)


class EvaluationProductionScaleRule(BaseRule):
    """Reject single BenchmarkCatalog-as-SFT placeholder datasets."""

    def __init__(self) -> None:
        self._count = 0

    @property
    def rule_id(self) -> str:
        return "EVL-003"

    @property
    def description(self) -> str:
        return "Evaluation SFT datasets must contain multiple judgment records."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.FATAL

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
        return ("evaluation",)

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
                        f"Evaluation dataset has {count} record(s); "
                        f"production minimum is {_MIN_PRODUCTION_RECORDS} "
                        "(single BenchmarkCatalog placeholder grain rejected)"
                    ),
                    dataset_name=dataset_name,
                ),
            )
        return ()
