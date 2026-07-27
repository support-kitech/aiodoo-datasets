"""Unit tests for the ValidationManager facade."""

import unittest

from validation.core.manager import ValidationManager


class TestValidationManager(unittest.TestCase):
    def test_summary(self) -> None:
        manager = ValidationManager()
        summary = manager.summary()
        self.assertEqual(summary["framework_version"], "1.0.0")
        self.assertGreater(summary["total_rules"], 0)
        self.assertGreater(summary["total_schemas"], 0)
        self.assertIn("registry_hash", summary)
        self.assertIn("schema_registry_hash", summary)
        self.assertIn("schema_ids", summary)

    def test_validate_record_planner_valid(self) -> None:
        manager = ValidationManager()
        record = {
            "instruction": "Build sale module",
            "input": "sale module context",
            "output": {"goal": "Create module", "summary": "Done", "tasks": [{"id": "t1"}]},
            "metadata": {"protocol_hash": "a" * 64, "module": "sale"},
        }
        result = manager.validate_record(record, "planner_v1_0.jsonl")
        self.assertEqual(result.status.value, "passed")

    def test_validate_record_context_valid(self) -> None:
        """Context records use id/query/artifacts/graph/metadata — NOT instruction/output."""
        manager = ValidationManager()
        record = {
            "id": "ctx_1",
            "query": {"query_id": "q1", "natural_language": "What is sale module?"},
            "artifacts": [],
            "graph": {"nodes": [], "edges": []},
            "metadata": {
                "protocol_hash": "b" * 64,
                "module": "sale",
                "protocol_version": "1.0",
            },
        }
        result = manager.validate_record(record, "context_v1_0.jsonl")
        self.assertEqual(result.status.value, "passed")

    def test_validate_record_approval_valid(self) -> None:
        """Approval records use subject-decision grain with stable identities."""
        manager = ValidationManager()
        record_id = "APR-" + ("a" * 32)
        record = {
            "review_id": record_id,
            "record_id": record_id,
            "capability": "coding",
            "subject_id": "coding:sale:abc",
            "source_object_id": "abc",
            "subject": "Approve coding artifact abc (sale)",
            "payload": {"capability": "coding", "evidence_count": 0},
            "decision": {
                "status": "APPROVED",
                "decision_id": "DEC-001",
                "confidence": "HIGH",
                "reasoning": "Good",
            },
            "findings": [],
            "evidence": [],
            "recommendations": [],
            "metadata": {
                "protocol_version": "1.0",
                "schema_version": "2.0",
                "source_module": "sale",
            },
        }
        result = manager.validate_record(record, "approval_dataset.jsonl")
        self.assertEqual(result.status.value, "passed")

    def test_validate_record_evaluation_valid(self) -> None:
        """Evaluation SFT records use judgment grain (candidate → verdict)."""
        manager = ValidationManager()
        record = {
            "record_id": "EVL-" + ("a" * 32),
            "candidate_id": "CAND-" + ("b" * 24),
            "evaluation_case_key": "pass",
            "capability_under_test": "coding",
            "candidate": {"capability": "coding", "output": {"goal": "x"}},
            "expectation": {"capability": "coding", "output": {"goal": "x"}},
            "rubric": "Judge coding quality",
            "verdict": "pass",
            "score": 1.0,
            "explanation": "Matches expectation",
            "metadata": {
                "protocol_version": "1.0",
                "schema_version": "2.0",
            },
        }
        result = manager.validate_record(record, "evaluation_dataset.jsonl")
        self.assertEqual(result.status.value, "passed")

    def test_validate_record_invalid(self) -> None:
        manager = ValidationManager()
        result = manager.validate_record({}, "test.jsonl")
        self.assertEqual(result.status.value, "failed")
        self.assertGreater(len(result.issues), 0)

    def test_validate_generator_output(self) -> None:
        manager = ValidationManager()
        records = [
            {
                "instruction": "Task 1",
                "input": "context",
                "output": {"goal": "G", "summary": "S", "tasks": [{"id": "t1"}]},
                "metadata": {"protocol_hash": "a" * 64, "module": "sale"},
            },
        ]
        result = manager.validate_generator_output(records, "planner")
        self.assertEqual(result.status.value, "passed")

    def test_validate_repository_context_none(self) -> None:
        manager = ValidationManager()
        result = manager.validate_repository_context(None)
        self.assertEqual(result.status.value, "failed")

    def test_validate_protocol_context_none(self) -> None:
        manager = ValidationManager()
        result = manager.validate_protocol_context(None)
        self.assertEqual(result.status.value, "failed")

    def test_registry_frozen(self) -> None:
        manager = ValidationManager()
        self.assertTrue(manager._registry.is_frozen)
        self.assertTrue(manager._schema_registry.is_frozen)


if __name__ == "__main__":
    unittest.main()
