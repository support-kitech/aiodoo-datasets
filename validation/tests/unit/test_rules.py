"""Unit tests for individual validation rules."""

import unittest
from pathlib import Path
from types import MappingProxyType

from validation.domain.models import ValidationContext
from validation.schemas.base import DatasetSchema, FieldDefinition
from validation.rules.schema.required_fields import RequiredFieldsRule
from validation.rules.schema.field_types import FieldTypeRule
from validation.rules.schema.record_structure import RecordStructureRule
from validation.rules.metadata.required_metadata import RequiredMetadataRule
from validation.rules.integrity.hash_verification import HashVerificationRule
from validation.rules.integrity.duplicate_detection import DuplicateDetectionRule
from validation.rules.integrity.deterministic_id import DeterministicIdRule
from validation.rules.references.circular_refs import CircularReferenceRule
from validation.rules.generators.context import ContextQueryRule
from validation.rules.generators.approval import ApprovalDecisionRule
from validation.rules.generators.evaluation import EvaluationCatalogRule


def _ctx(
    dataset: str = "test.jsonl",
    index: int = 0,
    schema: DatasetSchema | None = None,
) -> ValidationContext:
    meta: dict = {"current_dataset": dataset, "current_index": index}
    if schema is not None:
        meta["resolved_schema"] = schema
    return ValidationContext(
        dataset_dir=Path("."),
        metadata=MappingProxyType(meta),
    )


# Standard schema for planner-like records
_STD_SCHEMA = DatasetSchema(
    schema_id="test-std",
    generator_name="test",
    top_level_fields=(
        FieldDefinition(name="instruction", field_type=str, required=True),
        FieldDefinition(name="output", field_type=dict, required=True),
        FieldDefinition(name="metadata", field_type=dict, required=True),
    ),
    metadata_required_fields=("protocol_hash", "module"),
)

# Context schema
_CTX_SCHEMA = DatasetSchema(
    schema_id="context-v1",
    generator_name="context",
    top_level_fields=(
        FieldDefinition(name="id", field_type=str, required=True),
        FieldDefinition(name="query", field_type=dict, required=True),
        FieldDefinition(name="artifacts", field_type=list, required=True),
        FieldDefinition(name="graph", field_type=dict, required=True),
        FieldDefinition(name="metadata", field_type=dict, required=True),
    ),
    metadata_required_fields=("protocol_hash", "module"),
)


class TestRequiredFieldsRule(unittest.TestCase):
    def setUp(self) -> None:
        self.rule = RequiredFieldsRule()

    def test_valid_with_schema(self) -> None:
        record = {"instruction": "do x", "output": {}, "metadata": {}}
        issues = self.rule.validate(record, _ctx(schema=_STD_SCHEMA))
        self.assertEqual(len(issues), 0)

    def test_missing_instruction_with_schema(self) -> None:
        record = {"output": {}, "metadata": {}}
        issues = self.rule.validate(record, _ctx(schema=_STD_SCHEMA))
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].field_path, "instruction")

    def test_context_schema_valid(self) -> None:
        record = {"id": "x", "query": {}, "artifacts": [], "graph": {}, "metadata": {}}
        issues = self.rule.validate(record, _ctx(schema=_CTX_SCHEMA))
        self.assertEqual(len(issues), 0)

    def test_context_schema_missing_query(self) -> None:
        record = {"id": "x", "artifacts": [], "graph": {}, "metadata": {}}
        issues = self.rule.validate(record, _ctx(schema=_CTX_SCHEMA))
        self.assertEqual(len(issues), 1)

    def test_fallback_without_schema(self) -> None:
        """Without schema, falls back to instruction/output/metadata."""
        record = {}
        issues = self.rule.validate(record, _ctx())
        self.assertEqual(len(issues), 3)


class TestFieldTypeRule(unittest.TestCase):
    def setUp(self) -> None:
        self.rule = FieldTypeRule()

    def test_valid_types_with_schema(self) -> None:
        record = {"instruction": "x", "output": {}, "metadata": {}}
        self.assertEqual(len(self.rule.validate(record, _ctx(schema=_STD_SCHEMA))), 0)

    def test_wrong_type_with_schema(self) -> None:
        record = {"instruction": 123, "output": "str", "metadata": []}
        issues = self.rule.validate(record, _ctx(schema=_STD_SCHEMA))
        self.assertEqual(len(issues), 3)

    def test_context_schema_types(self) -> None:
        record = {"id": "x", "query": {}, "artifacts": [], "graph": {}, "metadata": {}}
        self.assertEqual(len(self.rule.validate(record, _ctx(schema=_CTX_SCHEMA))), 0)


class TestRecordStructureRule(unittest.TestCase):
    def setUp(self) -> None:
        self.rule = RecordStructureRule()

    def test_valid_with_schema(self) -> None:
        record = {"instruction": "x", "output": {}, "metadata": {}}
        self.assertEqual(len(self.rule.validate(record, _ctx(schema=_STD_SCHEMA))), 0)

    def test_unexpected_keys_with_schema(self) -> None:
        record = {"instruction": "x", "output": {}, "metadata": {}, "extra": True}
        issues = self.rule.validate(record, _ctx(schema=_STD_SCHEMA))
        self.assertEqual(len(issues), 1)

    def test_context_schema_allows_query(self) -> None:
        record = {"id": "x", "query": {}, "artifacts": [], "graph": {}, "metadata": {}}
        self.assertEqual(len(self.rule.validate(record, _ctx(schema=_CTX_SCHEMA))), 0)

    def test_context_schema_rejects_instruction(self) -> None:
        record = {
            "id": "x",
            "query": {},
            "artifacts": [],
            "graph": {},
            "metadata": {},
            "instruction": "bad",
        }
        issues = self.rule.validate(record, _ctx(schema=_CTX_SCHEMA))
        self.assertEqual(len(issues), 1)


class TestRequiredMetadataRule(unittest.TestCase):
    def setUp(self) -> None:
        self.rule = RequiredMetadataRule()

    def test_valid(self) -> None:
        record = {"metadata": {"protocol_hash": "abc123", "module": "sale"}}
        self.assertEqual(len(self.rule.validate(record, _ctx(schema=_STD_SCHEMA))), 0)

    def test_missing_hash(self) -> None:
        record = {"metadata": {"module": "sale"}}
        issues = self.rule.validate(record, _ctx(schema=_STD_SCHEMA))
        self.assertEqual(len(issues), 1)


class TestHashVerificationRule(unittest.TestCase):
    def setUp(self) -> None:
        self.rule = HashVerificationRule()

    def test_valid_sha256(self) -> None:
        record = {"metadata": {"protocol_hash": "a" * 64}}
        self.assertEqual(len(self.rule.validate(record, _ctx())), 0)

    def test_invalid_hash(self) -> None:
        record = {"metadata": {"protocol_hash": "not-a-hash"}}
        issues = self.rule.validate(record, _ctx())
        self.assertEqual(len(issues), 1)


class TestDuplicateDetectionRule(unittest.TestCase):
    def test_unique_hashes(self) -> None:
        rule = DuplicateDetectionRule()
        r1 = {"metadata": {"protocol_hash": "a" * 64}}
        r2 = {"metadata": {"protocol_hash": "b" * 64}}
        self.assertEqual(len(rule.validate(r1, _ctx())), 0)
        self.assertEqual(len(rule.validate(r2, _ctx())), 0)

    def test_duplicate_hash(self) -> None:
        rule = DuplicateDetectionRule()
        r = {"metadata": {"protocol_hash": "c" * 64}}
        self.assertEqual(len(rule.validate(r, _ctx())), 0)
        issues = rule.validate(r, _ctx())
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].rule_id, "INT-002")

    def test_reset(self) -> None:
        rule = DuplicateDetectionRule()
        r = {"metadata": {"protocol_hash": "d" * 64}}
        rule.validate(r, _ctx())
        rule.reset()
        self.assertEqual(len(rule.validate(r, _ctx())), 0)


class TestDeterministicIdRule(unittest.TestCase):
    def setUp(self) -> None:
        self.rule = DeterministicIdRule()

    def test_valid_ids(self) -> None:
        record = {"output": {"tasks": [{"id": "t1"}], "artifacts": [{"id": "a1"}]}}
        self.assertEqual(len(self.rule.validate(record, _ctx())), 0)

    def test_empty_task_id(self) -> None:
        record = {"output": {"tasks": [{"id": ""}]}}
        issues = self.rule.validate(record, _ctx())
        self.assertEqual(len(issues), 1)


class TestCircularReferenceRule(unittest.TestCase):
    def setUp(self) -> None:
        self.rule = CircularReferenceRule()

    def test_no_cycle(self) -> None:
        record = {
            "output": {
                "artifacts": [
                    {"id": "a", "dependencies": ["b"]},
                    {"id": "b", "dependencies": []},
                ]
            }
        }
        self.assertEqual(len(self.rule.validate(record, _ctx())), 0)

    def test_cycle(self) -> None:
        record = {
            "output": {
                "artifacts": [
                    {"id": "a", "dependencies": ["b"]},
                    {"id": "b", "dependencies": ["a"]},
                ]
            }
        }
        issues = self.rule.validate(record, _ctx())
        self.assertEqual(len(issues), 1)


class TestContextQueryRule(unittest.TestCase):
    def setUp(self) -> None:
        self.rule = ContextQueryRule()

    def test_valid_query(self) -> None:
        record = {"query": {"query_id": "q1", "natural_language": "What is X?"}}
        self.assertEqual(len(self.rule.validate(record, _ctx())), 0)

    def test_missing_query(self) -> None:
        record = {}
        issues = self.rule.validate(record, _ctx())
        self.assertEqual(len(issues), 1)

    def test_empty_query_fields(self) -> None:
        record = {"query": {"query_id": "", "natural_language": ""}}
        issues = self.rule.validate(record, _ctx())
        self.assertEqual(len(issues), 2)


class TestApprovalDecisionRule(unittest.TestCase):
    def setUp(self) -> None:
        self.rule = ApprovalDecisionRule()

    def test_valid_decision(self) -> None:
        record = {"decision": {"status": "approved", "decision_id": "D1"}}
        self.assertEqual(len(self.rule.validate(record, _ctx())), 0)

    def test_missing_decision(self) -> None:
        record = {}
        issues = self.rule.validate(record, _ctx())
        self.assertEqual(len(issues), 1)


class TestEvaluationCatalogRule(unittest.TestCase):
    def setUp(self) -> None:
        self.rule = EvaluationCatalogRule()

    def test_valid_catalog(self) -> None:
        record = {"catalog": {"catalog_id": "C1", "catalog_name": "Test"}}
        self.assertEqual(len(self.rule.validate(record, _ctx())), 0)

    def test_missing_catalog(self) -> None:
        record = {}
        issues = self.rule.validate(record, _ctx())
        self.assertEqual(len(issues), 1)


if __name__ == "__main__":
    unittest.main()
