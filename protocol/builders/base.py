"""Base builder utilities for the Protocol Framework."""

from protocol.domain.identifiers import ProtocolIdentifier


class IdentifierFactory:
    """
    Stateless factory for deterministic ProtocolIdentifier generation.

    All identifiers are derived from SHA-256 of canonical immutable values.
    Never uses UUID, randomness, time, or sequential counters.
    """

    @staticmethod
    def for_metadata(*components: str) -> ProtocolIdentifier:
        """Generate a deterministic identifier for a metadata object."""
        return ProtocolIdentifier.generate("metadata", *components)

    @staticmethod
    def for_reference(*components: str) -> ProtocolIdentifier:
        """Generate a deterministic identifier for a reference object."""
        return ProtocolIdentifier.generate("reference", *components)

    @staticmethod
    def for_relationship(*components: str) -> ProtocolIdentifier:
        """Generate a deterministic identifier for a relationship object."""
        return ProtocolIdentifier.generate("relationship", *components)

    @staticmethod
    def for_schema(*components: str) -> ProtocolIdentifier:
        """Generate a deterministic identifier for a schema object."""
        return ProtocolIdentifier.generate("schema", *components)

    @staticmethod
    def for_version(*components: str) -> ProtocolIdentifier:
        """Generate a deterministic identifier for a version object."""
        return ProtocolIdentifier.generate("version", *components)

    @staticmethod
    def for_manifest(*components: str) -> ProtocolIdentifier:
        """Generate a deterministic identifier for a manifest object."""
        return ProtocolIdentifier.generate("manifest", *components)

    @staticmethod
    def for_dataset(*components: str) -> ProtocolIdentifier:
        """Generate a deterministic identifier for a dataset object."""
        return ProtocolIdentifier.generate("dataset", *components)


class BaseBuilder:
    """
    Lightweight base builder for the Protocol Framework.

    Provides common typing and shared helper methods for deterministic
    builder operations. Business logic is strictly prohibited. Builders
    must remain stateless.
    """
    pass
