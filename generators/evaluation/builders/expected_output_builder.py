"""Expected Output Builder for Evaluation Generator."""

from typing import Tuple
from aiodoo_datasets.generators.evaluation.domain.expected_output import ExpectedOutput
from aiodoo_datasets.generators.evaluation.factories.expected_output_factory import (
    ExpectedOutputFactory,
)


class ExpectedOutputBuilder:
    """Builds ExpectedOutput objects securely."""

    @staticmethod
    def build(
        case_id: str, expected_value: str, value_type: str, required_elements: Tuple[str, ...] = ()
    ) -> ExpectedOutput:
        """Build expected output."""
        return ExpectedOutputFactory.create(
            case_id=case_id,
            expected_value=expected_value,
            value_type=value_type,
            required_elements=required_elements,
        )
