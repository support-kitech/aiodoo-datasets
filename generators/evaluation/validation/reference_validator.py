"""Reference Validator for Evaluation Generator."""

from aiodoo_datasets.generators.evaluation.exceptions import EvaluationValidationError
from aiodoo_datasets.generators.evaluation.domain.reference import Reference


class ReferenceValidator:
    """Validates references deterministically."""

    @staticmethod
    def validate(reference: Reference) -> None:
        """Fail-fast validation of a reference."""
        if not reference.source_generator:
            raise EvaluationValidationError("Reference must specify a source generator.")

        if not reference.source_reference:
            raise EvaluationValidationError("Reference must specify a source reference ID.")
