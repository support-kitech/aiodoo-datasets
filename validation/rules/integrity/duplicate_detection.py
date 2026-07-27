"""Rule: No duplicate records within a single dataset."""

import hashlib
import json

from validation.constants.framework import INTEGRITY_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule


class DuplicateDetectionRule(BaseRule):
    """
    Detects duplicate records within a dataset.

    Uses the record's natural identifier (id, review_id, evaluation_id)
    or falls back to a content hash. protocol_hash is NOT used because
    some generators (Context, Approval, Evaluation) share a single
    dataset-level protocol_hash across all records.

    NOTE: This rule is stateful at the dataset level. The DatasetValidator
    manages this lifecycle via reset().
    """

    def __init__(self) -> None:
        self._seen_ids: set[str] = set()

    @property
    def rule_id(self) -> str:
        return "INT-002"

    @property
    def description(self) -> str:
        return "No duplicate records within a single dataset."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.FATAL

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.INTEGRITY

    @property
    def priority(self) -> int:
        return INTEGRITY_RULE_PRIORITY + 1

    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        record_id = self._extract_record_id(record)

        if record_id in self._seen_ids:
            return (
                self._issue(
                    message=f"Duplicate record: '{record_id[:24]}...'",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="id",
                ),
            )
        self._seen_ids.add(record_id)
        return ()

    def reset(self) -> None:
        """Reset state for a new dataset validation pass."""
        self._seen_ids.clear()

    @staticmethod
    def _extract_record_id(record: dict) -> str:  # type: ignore[type-arg]
        """Extract the natural unique identifier from a record.

        Priority:
        1. Explicit 'id' field (Context generator)
        2. 'review_id' (Approval generator)
        3. 'evaluation_id' (Evaluation generator)
        4. Content hash fallback (Planner, Coding, Repair)
        """
        for key in ("record_id", "id", "review_id", "evaluation_id"):
            val = record.get(key)
            if isinstance(val, str) and val:
                return val

        # Fallback: deterministic content hash
        content = json.dumps(record, sort_keys=True, ensure_ascii=True)
        return hashlib.sha256(content.encode("utf-8")).hexdigest()
