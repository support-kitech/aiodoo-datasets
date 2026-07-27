"""Unit tests for eval-corpus contract validation routing."""

from __future__ import annotations

import json
from pathlib import Path
from types import MappingProxyType

from validation.builders.rule_builder import RuleBuilder
from validation.builders.schema_builder import SchemaBuilder
from validation.domain.enums import RuleScope, ValidationCategory, ValidationSeverity
from validation.domain.models import ValidationContext
from validation.rules.generators.eval_corpus import EvalCorpusContractRule
from validation.schemas.registry import infer_generator_from_filename


def _ctx(dataset: str = "coding_eval_corpus.jsonl", index: int = 0) -> ValidationContext:
    return ValidationContext(
        dataset_dir=Path("."),
        metadata=MappingProxyType({"current_dataset": dataset, "current_index": index}),
    )


class TestEvalCorpusFilenameRouting:
    def test_eval_corpus_wins_over_capability_substring(self) -> None:
        assert infer_generator_from_filename("coding_eval_corpus.jsonl") == "eval_corpus"
        assert infer_generator_from_filename("planner_eval_corpus.jsonl") == "eval_corpus"
        assert infer_generator_from_filename("coding_v1_0.jsonl") == "coding"

    def test_default_schema_resolves_eval_corpus(self) -> None:
        schema = SchemaBuilder.build_default().resolve_from_filename(
            "execution_eval_corpus.jsonl"
        )
        assert schema is not None
        assert schema.schema_id == "eval-corpus-v1"

    def test_default_rules_exclude_train_generator_rules(self) -> None:
        rules = RuleBuilder.build_default().get_rules_for_dataset("coding_eval_corpus.jsonl")
        rule_ids = {rule.rule_id for rule in rules}
        assert "EVC-001" in rule_ids
        assert "COD-001" not in rule_ids  # CodingArtifactsNonEmptyRule
        assert "CTR-002" not in rule_ids  # train-record contract projection for coding


class TestEvalCorpusContractRule:
    def setup_method(self) -> None:
        self.rule = EvalCorpusContractRule()

    def test_metadata(self) -> None:
        assert self.rule.rule_id == "EVC-001"
        assert self.rule.severity is ValidationSeverity.ERROR
        assert self.rule.category is ValidationCategory.CONTRACT
        assert self.rule.scope is RuleScope.GENERATOR_SPECIFIC
        assert self.rule.target_generators == ("eval_corpus",)

    def test_valid_corpus_record_from_disk_produces_no_issues(self) -> None:
        path = Path("datasets/coding_eval_corpus.jsonl")
        if not path.exists():
            return
        record = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
        assert self.rule.validate(record, _ctx()) == ()

    def test_unknown_capability_fails(self) -> None:
        record = {
            "capability": "not-a-capability",
            "request": {},
            "expected_response": {},
            "source_protocol_hash": None,
        }
        issues = self.rule.validate(record, _ctx())
        assert len(issues) == 1
        assert "Unknown capability" in issues[0].message
