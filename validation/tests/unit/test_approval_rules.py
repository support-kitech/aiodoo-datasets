"""Unit tests for Approval generator-specific validation rules."""

from __future__ import annotations

from pathlib import Path

from validation.domain.models import ValidationContext
from validation.rules.generators.approval import (
    ApprovalBoundedEvidenceRule,
    ApprovalIdentityRule,
    ApprovalProductionScaleRule,
)


def _ctx(dataset: str = "approval_dataset.jsonl", index: int = 0) -> ValidationContext:
    return ValidationContext(
        dataset_dir=Path("."),
        metadata={"current_dataset": dataset, "current_index": index},
    )


def test_identity_rule_accepts_valid_record() -> None:
    record_id = "APR-" + ("c" * 32)
    record = {
        "record_id": record_id,
        "review_id": record_id,
        "capability": "planner",
        "subject_id": "planner:m:h",
        "source_object_id": "h",
        "subject": "Approve planner artifact h (m)",
    }
    issues = ApprovalIdentityRule().validate(record, _ctx())
    assert issues == ()


def test_bounded_evidence_rule_rejects_overflow() -> None:
    record = {"evidence": [{}] * 40}
    issues = ApprovalBoundedEvidenceRule().validate(record, _ctx())
    assert len(issues) == 1
    assert issues[0].rule_id == "APR-003"


def test_production_scale_finalize_rejects_placeholder() -> None:
    rule = ApprovalProductionScaleRule()
    rule.reset()
    rule.validate({"record_id": "x"}, _ctx())
    issues = rule.finalize(dataset_name="approval_dataset.jsonl", records_validated=1)
    assert len(issues) == 1
    assert issues[0].rule_id == "APR-004"
