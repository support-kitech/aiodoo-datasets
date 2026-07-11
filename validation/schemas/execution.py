"""Schema definition for the Execution generator dataset."""

from validation.schemas.base import DatasetSchema, FieldDefinition

EXECUTION_SCHEMA = DatasetSchema(
    schema_id="execution-v1",
    generator_name="execution",
    version="1.0.0",
    description="Execution generator: instruction/output/metadata (standard format)",
    top_level_fields=(
        FieldDefinition(name="instruction", field_type=str, required=True),
        FieldDefinition(name="output", field_type=dict, required=True),
        FieldDefinition(name="metadata", field_type=dict, required=True),
        FieldDefinition(name="context", field_type=dict, required=False),
    ),
    metadata_required_fields=("protocol_hash", "module"),
)
