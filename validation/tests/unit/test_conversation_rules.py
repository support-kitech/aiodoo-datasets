"""Unit tests for Conversation generator-specific validation rules."""

from __future__ import annotations

from pathlib import Path

from validation.domain.models import ValidationContext
from validation.rules.generators.conversation import (
    ConversationBoundedHistoryRule,
    ConversationIdentityRule,
    ConversationProductionScaleRule,
)


def _ctx(dataset: str = "conversation_dataset.jsonl", index: int = 0) -> ValidationContext:
    return ValidationContext(
        dataset_dir=Path("."),
        metadata={"current_dataset": dataset, "current_index": index},
    )


def test_identity_rule_accepts_valid_record() -> None:
    record = {
        "record_id": "CNV-" + ("a" * 32),
        "conversation_id": "CONV-" + ("b" * 24),
        "turn_index": 0,
    }
    assert ConversationIdentityRule().validate(record, _ctx()) == ()


def test_bounded_history_rejects_non_assistant_reply() -> None:
    record = {
        "output": {
            "turns": [
                {
                    "messages": [
                        {"role": "user", "content": "hi"},
                        {"role": "user", "content": "again"},
                    ]
                }
            ]
        }
    }
    issues = ConversationBoundedHistoryRule().validate(record, _ctx())
    assert len(issues) == 1
    assert issues[0].rule_id == "CNV-003"


def test_production_scale_finalize_rejects_placeholder() -> None:
    rule = ConversationProductionScaleRule()
    rule.reset()
    rule.validate({"record_id": "x"}, _ctx())
    issues = rule.finalize(dataset_name="conversation_dataset.jsonl", records_validated=1)
    assert len(issues) == 1
    assert issues[0].rule_id == "CNV-004"
