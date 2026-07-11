"""Schema definition for the Coding generator dataset."""

from validation.schemas.base import DatasetSchema, FieldDefinition

CODING_SCHEMA = DatasetSchema(
    schema_id="coding-v1",
    generator_name="coding",
    version="1.0.0",
    description="Coding generator: instruction/context/output(ArtifactPayload)/metadata",
    top_level_fields=(
        FieldDefinition(name="instruction", field_type=str, required=True),
        FieldDefinition(name="context", field_type=dict, required=True),
        FieldDefinition(name="output", field_type=dict, required=True),
        FieldDefinition(name="metadata", field_type=dict, required=True),
    ),
    metadata_required_fields=("protocol_hash", "module"),
)
