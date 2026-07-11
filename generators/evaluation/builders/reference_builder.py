"""Reference Builder for Evaluation Generator."""

from generators.evaluation.domain.reference import Reference
from generators.evaluation.factories.reference_factory import ReferenceFactory


class ReferenceBuilder:
    """Builds Reference objects securely."""

    @staticmethod
    def build(source_generator: str, source_reference: str, description: str) -> Reference:
        """Build reference."""
        return ReferenceFactory.create(
            source_generator=source_generator,
            source_reference=source_reference,
            description=description,
        )
