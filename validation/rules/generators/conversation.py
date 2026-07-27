"""Generator-specific validation rules for the Conversation dataset."""

from __future__ import annotations

import re

from validation.constants.framework import GENERATOR_RULE_PRIORITY
from validation.domain.enums import ValidationSeverity, ValidationCategory, RuleScope
from validation.domain.models import ValidationIssue, ValidationContext
from validation.rules.base import BaseRule

_MAX_HISTORY_MESSAGES = 16
_MIN_PRODUCTION_RECORDS = 2
_RECORD_ID_RE = re.compile(r"^CNV-[0-9a-f]{32}$")
_CONVERSATION_ID_RE = re.compile(r"^CONV-[0-9a-f]{24}$")


class ConversationInstructionRule(BaseRule):
    """Conversation record must contain a non-empty instruction."""

    @property
    def rule_id(self) -> str:
        return "CNV-001"

    @property
    def description(self) -> str:
        return "Conversation record must contain a non-empty instruction."

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
        return ("conversation",)

    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        instruction = record.get("instruction", "")
        if not instruction or not isinstance(instruction, str) or not instruction.strip():
            return (
                self._issue(
                    message="Conversation record has empty instruction",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="instruction",
                ),
            )
        return ()


class ConversationIdentityRule(BaseRule):
    """Conversation records must carry stable Step 2.1 identities."""

    @property
    def rule_id(self) -> str:
        return "CNV-002"

    @property
    def description(self) -> str:
        return "Conversation record_id/conversation_id/turn_index must be well-formed."

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
        return ("conversation",)

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
                    message="Conversation record_id must match CNV-<32 hex> scheme",
                    dataset_name=ds,  # type: ignore[arg-type]
                    record_index=idx,  # type: ignore[arg-type]
                    field_path="record_id",
                )
            )

        conversation_id = record.get("conversation_id")
        if not isinstance(conversation_id, str) or not _CONVERSATION_ID_RE.match(conversation_id):
            issues.append(
                self._issue(
                    message="Conversation conversation_id must match CONV-<24 hex> scheme",
                    dataset_name=ds,  # type: ignore[arg-type]
                    record_index=idx,  # type: ignore[arg-type]
                    field_path="conversation_id",
                )
            )

        turn_index = record.get("turn_index")
        if not isinstance(turn_index, int) or turn_index < 0:
            issues.append(
                self._issue(
                    message="Conversation turn_index must be a non-negative integer",
                    dataset_name=ds,  # type: ignore[arg-type]
                    record_index=idx,  # type: ignore[arg-type]
                    field_path="turn_index",
                )
            )

        return tuple(issues)


class ConversationBoundedHistoryRule(BaseRule):
    """History in a Conversation training record must be bounded."""

    @property
    def rule_id(self) -> str:
        return "CNV-003"

    @property
    def description(self) -> str:
        return "Conversation request history must not exceed the production bound."

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
        return ("conversation",)

    def validate(
        self,
        record: dict,
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        output = record.get("output")
        if not isinstance(output, dict):
            return (
                self._issue(
                    message="Conversation output must be an object",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="output",
                ),
            )

        messages: list[dict] = []
        for turn in output.get("turns", []) if isinstance(output.get("turns"), list) else []:
            if not isinstance(turn, dict):
                continue
            for message in (
                turn.get("messages", []) if isinstance(turn.get("messages"), list) else []
            ):
                if isinstance(message, dict):
                    messages.append(message)

        if len(messages) < 2:
            return (
                self._issue(
                    message="Conversation record must contain prefix + assistant reply messages",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="output.turns",
                ),
            )

        # Prefix is all but last message; last must be assistant.
        prefix_len = len(messages) - 1
        if prefix_len > _MAX_HISTORY_MESSAGES:
            return (
                self._issue(
                    message=(
                        f"Conversation history length {prefix_len} exceeds "
                        f"bound {_MAX_HISTORY_MESSAGES}"
                    ),
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="output.turns",
                ),
            )

        last_role = str(messages[-1].get("role", "")).lower()
        if last_role != "assistant":
            return (
                self._issue(
                    message="Conversation reply (last message) must have role assistant",
                    dataset_name=context.metadata.get("current_dataset", ""),  # type: ignore[arg-type]
                    record_index=context.metadata.get("current_index"),  # type: ignore[arg-type]
                    field_path="output.turns",
                ),
            )
        return ()


class ConversationProductionScaleRule(BaseRule):
    """Reject single integrated-conversation placeholder datasets."""

    def __init__(self) -> None:
        self._count = 0

    @property
    def rule_id(self) -> str:
        return "CNV-004"

    @property
    def description(self) -> str:
        return "Conversation production datasets must contain multiple next-reply records."

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
        return ("conversation",)

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
                        f"Conversation dataset has {count} record(s); "
                        f"production minimum is {_MIN_PRODUCTION_RECORDS} "
                        "(single integrated conversation grain rejected)"
                    ),
                    dataset_name=dataset_name,
                ),
            )
        return ()
