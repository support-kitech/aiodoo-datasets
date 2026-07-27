"""Rules for contract-shaped ``*_eval_corpus.jsonl`` records.

These files are not training rows. Each line is a gold
``(request, expected_response)`` pair already projected onto
``aiodoo_contract`` schemas (see
:mod:`generators.common.contract.eval_corpus`). Validation therefore
re-hydrates those payloads and runs :class:`ContractValidator` rather than
attempting train-record projection via :func:`project_record`.
"""

from __future__ import annotations

from typing import Any

from aiodoo_contract.schemas.enums import CapabilityName
from aiodoo_contract.schemas.registry import request_schema_for, response_schema_for
from aiodoo_contract.validators import ContractValidator
from pydantic import ValidationError

from validation.constants.framework import CONTRACT_RULE_PRIORITY
from validation.domain.enums import RuleScope, ValidationCategory, ValidationSeverity
from validation.domain.models import ValidationContext, ValidationIssue
from validation.rules.base import BaseRule

__all__ = ["EvalCorpusContractRule"]

_contract_validator = ContractValidator()


class EvalCorpusContractRule(BaseRule):
    """Validate eval-corpus request/response payloads against ``aiodoo_contract``."""

    @property
    def rule_id(self) -> str:
        return "EVC-001"

    @property
    def description(self) -> str:
        return (
            "Eval corpus request/expected_response must rehydrate and pass "
            "aiodoo_contract ContractValidator."
        )

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.ERROR

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.CONTRACT

    @property
    def priority(self) -> int:
        return CONTRACT_RULE_PRIORITY

    @property
    def scope(self) -> RuleScope:
        return RuleScope.GENERATOR_SPECIFIC

    @property
    def target_generators(self) -> tuple[str, ...]:
        return ("eval_corpus",)

    def validate(
        self,
        record: dict[str, Any],
        context: ValidationContext,  # type: ignore[type-arg]
    ) -> tuple[ValidationIssue, ...]:
        ds_name = context.metadata.get("current_dataset", "")
        rec_idx = context.metadata.get("current_index")
        issues: list[ValidationIssue] = []

        capability_raw = record.get("capability")
        request_data = record.get("request")
        response_data = record.get("expected_response")

        if not isinstance(capability_raw, str) or not capability_raw.strip():
            return (
                self._issue(
                    message="Eval corpus record has missing or empty 'capability'",
                    dataset_name=ds_name,  # type: ignore[arg-type]
                    record_index=rec_idx,  # type: ignore[arg-type]
                    field_path="capability",
                ),
            )

        try:
            capability = CapabilityName(capability_raw)
        except ValueError:
            return (
                self._issue(
                    message=f"Unknown capability for eval corpus: {capability_raw!r}",
                    dataset_name=ds_name,  # type: ignore[arg-type]
                    record_index=rec_idx,  # type: ignore[arg-type]
                    field_path="capability",
                ),
            )

        if not isinstance(request_data, dict):
            return (
                self._issue(
                    message="Eval corpus 'request' must be a JSON object",
                    dataset_name=ds_name,  # type: ignore[arg-type]
                    record_index=rec_idx,  # type: ignore[arg-type]
                    field_path="request",
                ),
            )
        if not isinstance(response_data, dict):
            return (
                self._issue(
                    message="Eval corpus 'expected_response' must be a JSON object",
                    dataset_name=ds_name,  # type: ignore[arg-type]
                    record_index=rec_idx,  # type: ignore[arg-type]
                    field_path="expected_response",
                ),
            )

        try:
            request = request_schema_for(capability).model_validate(request_data)
            response = response_schema_for(capability).model_validate(response_data)
        except (ValidationError, KeyError, TypeError, ValueError) as exc:
            return (
                self._issue(
                    message=f"Could not rehydrate eval corpus contract payloads: {exc}",
                    dataset_name=ds_name,  # type: ignore[arg-type]
                    record_index=rec_idx,  # type: ignore[arg-type]
                    field_path="request",
                ),
            )

        request_result = _contract_validator.validate_request(request)
        response_result = _contract_validator.validate_response(response)
        for label, result in (("request", request_result), ("expected_response", response_result)):
            if not result.valid:
                for contract_issue in result.issues:
                    issues.append(
                        self._issue(
                            message=(
                                f"aiodoo_contract {label} validation: {contract_issue.message}"
                            ),
                            dataset_name=ds_name,  # type: ignore[arg-type]
                            record_index=rec_idx,  # type: ignore[arg-type]
                            field_path=contract_issue.path or label,
                        )
                    )
        return tuple(issues)
