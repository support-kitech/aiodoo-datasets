"""Evaluation Rule Factory for Evaluation Generator."""

import hashlib
from typing import Tuple
from aiodoo_datasets.generators.evaluation.domain.evaluation_rule import EvaluationRule


class RuleFactory:
    """Factory for creating immutable EvaluationRule objects with deterministic IDs."""

    @staticmethod
    def generate_id(case_id: str, sequence_index: int) -> str:
        """Generate a deterministic rule ID."""
        hash_input = f"RULE:{case_id}:{sequence_index}"
        rule_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
        return f"RULE-{rule_hash}"

    @staticmethod
    def create(
        case_id: str,
        sequence_index: int,
        description: str,
        rule_type: str,
        parameters: Tuple[str, ...] = (),
    ) -> EvaluationRule:
        """Create a new evaluation rule with a hash-based deterministic ID."""
        rule_id = RuleFactory.generate_id(case_id, sequence_index)

        return EvaluationRule(
            rule_id=rule_id, description=description, rule_type=rule_type, parameters=parameters
        )
