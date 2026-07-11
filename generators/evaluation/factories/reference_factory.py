"""Reference Factory for Evaluation Generator."""

from aiodoo_datasets.generators.evaluation.domain.reference import Reference

class ReferenceFactory:
    """Factory for creating immutable Reference objects."""
    
    @staticmethod
    def create(source_generator: str, source_reference: str, description: str) -> Reference:
        """Create a reference."""
        return Reference(
            source_generator=source_generator,
            source_reference=source_reference,
            description=description
        )
