"""Base schema definition for generator-aware validation."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FieldDefinition:
    """Immutable definition of a single field in a dataset record."""

    name: str
    field_type: type | tuple[type, ...] = object
    required: bool = True
    description: str = ""


@dataclass(frozen=True, slots=True)
class DatasetSchema:
    """
    Immutable schema describing the record structure of a specific generator.

    Each generator produces records with a unique structure.
    The schema defines which top-level and metadata fields are expected.
    """

    schema_id: str
    generator_name: str
    version: str = "1.0.0"
    top_level_fields: tuple[FieldDefinition, ...] = ()
    metadata_required_fields: tuple[str, ...] = ()
    description: str = ""

    @property
    def required_field_names(self) -> frozenset[str]:
        """Return the set of required top-level field names."""
        return frozenset(f.name for f in self.top_level_fields if f.required)

    @property
    def optional_field_names(self) -> frozenset[str]:
        """Return the set of optional top-level field names."""
        return frozenset(f.name for f in self.top_level_fields if not f.required)

    @property
    def all_field_names(self) -> frozenset[str]:
        """Return the set of all allowed top-level field names."""
        return frozenset(f.name for f in self.top_level_fields)

    def get_field(self, name: str) -> FieldDefinition | None:
        """Look up a field definition by name."""
        for f in self.top_level_fields:
            if f.name == name:
                return f
        return None
