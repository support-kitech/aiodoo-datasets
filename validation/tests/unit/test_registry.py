"""Unit tests for the RuleRegistry."""

import unittest

from validation.domain.enums import ValidationSeverity, ValidationCategory
from validation.domain.models import ValidationIssue, ValidationContext
from validation.exceptions import ValidationError
from validation.rules.base import BaseRule
from validation.rules.registry import RuleRegistry


class DummyRule(BaseRule):
    """A test rule for registry tests."""

    def __init__(self, rid: str = "TEST-001", pri: int = 10, gens: tuple[str, ...] = ()) -> None:
        self._id = rid
        self._pri = pri
        self._gens = gens

    @property
    def rule_id(self) -> str:
        return self._id

    @property
    def description(self) -> str:
        return "Test rule"

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.ERROR

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.SCHEMA

    @property
    def priority(self) -> int:
        return self._pri

    @property
    def target_generators(self) -> tuple[str, ...]:
        return self._gens

    def validate(self, record: dict, context: ValidationContext) -> tuple[ValidationIssue, ...]:
        return ()


class TestRuleRegistry(unittest.TestCase):
    def test_register_and_freeze(self) -> None:
        reg = RuleRegistry()
        reg.register(DummyRule("A", 20))
        reg.register(DummyRule("B", 10))
        reg.freeze()
        self.assertTrue(reg.is_frozen)
        # Should be sorted by priority
        self.assertEqual(reg.all_rules[0].rule_id, "B")
        self.assertEqual(reg.all_rules[1].rule_id, "A")

    def test_duplicate_raises(self) -> None:
        reg = RuleRegistry()
        reg.register(DummyRule("X"))
        with self.assertRaises(ValidationError):
            reg.register(DummyRule("X"))

    def test_frozen_mutation_raises(self) -> None:
        reg = RuleRegistry()
        reg.freeze()
        with self.assertRaises(ValidationError):
            reg.register(DummyRule("Y"))

    def test_generator_filtering(self) -> None:
        reg = RuleRegistry()
        reg.register(DummyRule("UNI-001", gens=()))  # Universal
        reg.register(DummyRule("PLN-001", gens=("planner",)))  # Planner-specific
        reg.register(DummyRule("COD-001", gens=("coding",)))  # Coding-specific
        reg.register(DummyRule("EVC-001", gens=("eval_corpus",)))  # Eval corpus
        reg.freeze()

        planner_rules = reg.get_rules_for_dataset("planner_v1_0.jsonl")
        self.assertEqual(len(planner_rules), 2)  # UNI + PLN
        rule_ids = {r.rule_id for r in planner_rules}
        self.assertIn("UNI-001", rule_ids)
        self.assertIn("PLN-001", rule_ids)
        self.assertNotIn("COD-001", rule_ids)
        self.assertNotIn("EVC-001", rule_ids)

        eval_rules = reg.get_rules_for_dataset("coding_eval_corpus.jsonl")
        eval_ids = {r.rule_id for r in eval_rules}
        self.assertIn("UNI-001", eval_ids)
        self.assertIn("EVC-001", eval_ids)
        self.assertNotIn("COD-001", eval_ids)
        self.assertNotIn("PLN-001", eval_ids)

    def test_hash_deterministic(self) -> None:
        reg1 = RuleRegistry()
        reg1.register(DummyRule("A"))
        reg1.register(DummyRule("B"))
        reg1.freeze()

        reg2 = RuleRegistry()
        reg2.register(DummyRule("A"))
        reg2.register(DummyRule("B"))
        reg2.freeze()

        self.assertEqual(reg1.hash_value, reg2.hash_value)

    def test_register_many(self) -> None:
        reg = RuleRegistry()
        reg.register_many(DummyRule("A"), DummyRule("B"), DummyRule("C"))
        reg.freeze()
        self.assertEqual(len(reg.all_rules), 3)


if __name__ == "__main__":
    unittest.main()
