"""Unit tests for Evaluation validation rules."""

from __future__ import annotations

from pathlib import Path

from validation.domain.models import ValidationContext
from validation.rules.generators.evaluation import (
    EvaluationIdentityRule,
    EvaluationProductionScaleRule,
)


def _ctx(dataset: str = "evaluation_dataset.jsonl", index: int = 0) -> ValidationContext:
    return ValidationContext(
        dataset_dir=Path("."),
        metadata={"current_dataset": dataset, "current_index": index},
    )


def test_identity_rule_accepts_valid_judgment() -> None:
    record = {
        "record_id": "EVL-" + ("c" * 32),
        "candidate_id": "CAND-" + ("d" * 24),
        "evaluation_case_key": "fail",
        "verdict": "fail",
        "candidate": {"capability": "repair"},
    }
    assert EvaluationIdentityRule().validate(record, _ctx()) == ()


def test_production_scale_rejects_placeholder() -> None:
    rule = EvaluationProductionScaleRule()
    rule.reset()
    rule.validate({"record_id": "x"}, _ctx())
    issues = rule.finalize(dataset_name="evaluation_dataset.jsonl", records_validated=1)
    assert len(issues) == 1
    assert issues[0].rule_id == "EVL-003"
