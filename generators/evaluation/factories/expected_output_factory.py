"""Expected Output Factory for Evaluation Generator."""

import hashlib
from typing import Tuple
from aiodoo_datasets.generators.evaluation.domain.expected_output import ExpectedOutput


class ExpectedOutputFactory:
    """Factory for creating immutable ExpectedOutput objects with deterministic IDs."""

    @staticmethod
    def generate_id(case_id: str) -> str:
        """Generate a deterministic expected output ID."""
        hash_input = f"EXPOUT:{case_id}"
        out_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
        return f"EXPOUT-{out_hash}"

    @staticmethod
    def create(
        case_id: str, expected_value: str, value_type: str, required_elements: Tuple[str, ...] = ()
    ) -> ExpectedOutput:
        """Create a new expected output with a hash-based deterministic ID."""
        output_id = ExpectedOutputFactory.generate_id(case_id)

        return ExpectedOutput(
            output_id=output_id,
            expected_value=expected_value,
            value_type=value_type,
            required_elements=required_elements,
        )
